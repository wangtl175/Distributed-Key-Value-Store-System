import threading
import json
import random
import os
import argparse
import MasterServer_pb2
import MasterServer_pb2_grpc
import grpc
import time
from concurrent import futures
import sys

sys.path.append('../')
sys.path.append('../ChunkServer')
from ChunkServer import ChunkServer_pb2
from ChunkServer import ChunkServer_pb2_grpc
import settings


# 主节点，不存储key-value，只保存哪个key保存在哪个chunk server上
# 同时决定新插入的key-value堆的插入位置


class MasterServer(MasterServer_pb2_grpc.MasterServerServicer):
    def __init__(self, id, ip, port, role='primary', primary_ip=None, primary_port=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.role = role  # 判断是否是主节点
        self.primary_ip = primary_ip
        self.primary_port = primary_port
        self.secondaries = {}
        self.directory_mutex = threading.Lock()
        self.chunks_mutex = threading.Lock()
        self.secondaries_mutex = threading.Lock()
        if self.role == 'primary':
            if os.path.exists(settings.Directory_File):
                with open(settings.Directory_File, 'r') as file:
                    self.directory = json.load(file)
            else:
                self.directory = {}
            if os.path.exists(settings.Chunk_List_File):
                with open(settings.Chunk_List_File, 'r') as file:
                    self.chunks = json.load(file)
            else:
                self.chunks = {}  # key是节点id，value可以记录一些节点的信息，例如key数量等
        else:
            self.chunks = {}
            self.directory = {}
            with grpc.insecure_channel('{}:{}'.format(self.primary_ip, self.primary_port)) as channel:
                stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                response = stub.sync_chunks(MasterServer_pb2.Empty())
                for chunk in response:
                    self.chunks[chunk.id] = {'ip': chunk.ip, 'port': chunk.port, 'num_keys': chunk.num_keys,
                                             'live': True}
                response = stub.sync_directory(MasterServer_pb2.Empty())
                for item in response:
                    self.directory[item.key] = item.chunk
                stub.add_secondary(MasterServer_pb2.Secondary(id=self.id, ip=self.ip, port=self.port))

    # 后继由从节点来同步
    def add_secondary(self, request, context):
        self.secondaries_mutex.acquire()
        if request.id in self.secondaries:
            self.secondaries_mutex.release()
            return MasterServer_pb2.Reply(msg='secondary node existed', code=400)
        self.secondaries[request.id] = {'ip': request.ip, 'port': request.port, 'live': True}
        self.secondaries_mutex.release()
        return MasterServer_pb2.Reply(msg=request.ip, code=200)

    def _persistence(self):
        while True:
            with open(settings.Directory_File, 'w') as file:
                json.dump(self.directory, file)
            with open(settings.Chunk_List_File, 'w') as file:
                json.dump(self.chunks, file)
            with open(settings.Info_File, 'w') as file:
                info = {'id': self.id, 'ip': self.ip, 'port': self.port, 'role': self.role,
                        'primary_ip': self.primary_ip, 'primary_port': self.primary_port}
                json.dump(info, file)
            # time.sleep(3600)
            time.sleep(settings.Persistence_Time)

    def sync_directory(self, request, context):
        for key in self.directory:
            yield MasterServer_pb2.Directory(key=key, chunk=self.directory[key], msg='ok', code=200)

    def sync_chunks(self, request, context):
        for chunk in self.chunks:
            yield MasterServer_pb2.Chunk(id=chunk, ip=self.chunks[chunk]['ip'], port=self.chunks[chunk]['port'],
                                         num_keys=self.chunks[chunk]['num_keys'], msg='ok', code=200)

    def _update_secondaries(self, operation, *args, **kwargs):
        for secondary in list(self.secondaries.keys()):
            try:
                with grpc.insecure_channel('{}:{}'.format(self.secondaries[secondary]['ip'],
                                                          self.secondaries[secondary]['port'])) as channel:
                    stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                    opt = getattr(stub, operation)
                    # response = opt(*args, **kwargs)
                    opt(*args, **kwargs)
                    # print(response.msg, response.code)
            except Exception as e:
                print(e)
                del self.secondaries[secondary]

    # 获取chunk的id
    def get_chunk(self, request, context):
        if request.key in self.directory:
            chunk = self.directory[request.key]
            return MasterServer_pb2.Chunk(id=chunk, ip=self.chunks[chunk]['ip'], port=self.chunks[chunk]['port'],
                                          msg='ok', code=200)
        else:
            return MasterServer_pb2.Chunk(msg='not found', code=404)

    def add_chunk(self, request, context):
        self.chunks_mutex.acquire()
        if request.id in self.chunks:
            self.chunks_mutex.release()
            return MasterServer_pb2.Reply(msg='chunk existed', code=400)
        else:
            self.chunks[request.id] = {'ip': request.ip, 'port': request.port, 'num_keys': request.num_keys,
                                       'live': True}
            # self.chunks_mutex.release()
            self._update_secondaries('add_chunk', request)
            self.chunks_mutex.release()  # 要更新完从节点才释放锁，否则会导致从节点和主节点不一致
            return MasterServer_pb2.Reply(msg=request.id, code=200)

    # 当一个chunk的从节点发现主节点失效时，选出新的主节点，然后告诉master，然后master更新自己的directory
    def replace_chunk(self, request, context):
        self.directory_mutex.acquire()
        self.chunks_mutex.acquire()
        for key in list(self.directory.keys()):
            if self.directory[key] == request.old_chunk.id:
                del self.directory[key]
        del self.chunks[request.old_chunk.id]
        self.chunks[request.new_chunk.id] = {'ip': request.new_chunk.ip, 'port': request.new_chunk.port,
                                             'num_keys': request.new_chunk.num_keys, 'live': True}
        with grpc.insecure_channel('{}:{}'.format(request.new_chunk.ip, request.new_chunk.port)) as channel:
            stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
            response = stub.sync_tables(ChunkServer_pb2.Empty())
            for res in response:
                self.directory[res.key] = request.new_chunk.id
        self._update_secondaries('replace_chunk', request)
        self.chunks_mutex.release()
        self.directory_mutex.release()
        return MasterServer_pb2.Reply(msg='success', code=200)

    # 随机选取
    def _select_chunk(self):
        live = []
        for chunk in self.chunks:
            if self.chunks[chunk]['live']:
                live.append(chunk)
        if len(live) == 0:
            return None
        else:
            return random.choice(live)

    def insert_key(self, request, context):
        self.directory_mutex.acquire()
        if request.key in self.directory:
            self.directory_mutex.release()
            return MasterServer_pb2.Chunk(msg='key existed', code=400)
        else:
            chunk = request.chunk
            if chunk == '':
                chunk = self._select_chunk()
                request.chunk = chunk
            if chunk:
                self.directory[request.key] = chunk
                self.chunks[chunk]['num_keys'] += 1
                self._update_secondaries('insert_key', request)
                self.directory_mutex.release()
                return MasterServer_pb2.Chunk(id=chunk, ip=self.chunks[chunk]['ip'], port=self.chunks[chunk]['port'],
                                              code=200)
            else:
                self.directory_mutex.release()
                return MasterServer_pb2.Chunk(msg='chunk is unavailable', code=500)

    def delete_key(self, request, context):
        self.directory_mutex.acquire()
        if request.key not in self.directory:
            self.directory_mutex.release()
            return MasterServer_pb2.Chunk(msg='key do not exist', code=404)
        else:
            chunk = self.directory[request.key]
            if self.chunks[chunk]['live']:
                del self.directory[request.key]
                self.chunks[chunk]['num_keys'] -= 1
                self._update_secondaries('delete_key', request)
                self.directory_mutex.release()
                return MasterServer_pb2.Chunk(id=chunk, ip=self.chunks[chunk]['ip'], port=self.chunks[chunk]['port'],
                                              code=200)
            else:
                self.directory_mutex.release()
                return MasterServer_pb2.Chunk(msg='chunk is unavailable', code=500)

    # 检测节点的心跳
    def _detect_heart(self):
        while True:
            for secondary in list(self.secondaries.keys()):
                try:
                    with grpc.insecure_channel('{}:{}'.format(self.secondaries[secondary]['ip'],
                                                              self.secondaries[secondary]['port'])) as channel:
                        stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                        response = stub.heart(MasterServer_pb2.Empty())
                        if response.code != 200:
                            del self.secondaries[secondary]
                except Exception as e:
                    print(e)
                    del self.secondaries[secondary]
            for chunk in self.chunks:
                try:
                    with grpc.insecure_channel(
                            '{}:{}'.format(self.chunks[chunk]['ip'], self.chunks[chunk]['port'])) as channel:
                        stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                        response = stub.heart(ChunkServer_pb2.Empty())
                        if response.code == 200:
                            self.chunks[chunk]['live'] = True
                        else:
                            self.chunks[chunk]['live'] = False
                except Exception as e:
                    print(e)
                    self.chunks[chunk]['live'] = False
            time.sleep(settings.Detect_Heart_Time)

    def get_primary(self, request, context):
        if self.role == 'primary':
            return MasterServer_pb2.Primary(ip=self.ip, port=self.port)
        else:
            return MasterServer_pb2.Primary(id=self.primary_ip, port=self.port)

    # 自己的心跳
    # def heart(self):
    def heart(self, request, context):
        return MasterServer_pb2.Reply(msg='I am master', code=200)

    def run(self):
        detect_heart = threading.Thread(target=self._detect_heart)
        detect_heart.setDaemon(True)
        detect_heart.start()
        persistence = threading.Thread(target=self._persistence)
        persistence.setDaemon(True)
        persistence.start()
        persistence.join()
        detect_heart.join()


def run_server(id, ip, port, role='primary', primary_ip=None, primary_port=None):
    master = MasterServer(id=id, ip=ip, port=port, role=role, primary_ip=primary_ip, primary_port=primary_port)
    master_run = threading.Thread(target=master.run)
    master_run.setDaemon(True)
    master_run.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MasterServer_pb2_grpc.add_MasterServerServicer_to_server(master, server)
    server.add_insecure_port('{}:{}'.format(master.ip, master.port))
    print('Master server start')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id', type=str)
    parser.add_argument('ip', help='ip', type=str)
    parser.add_argument('port', help='port', type=str)
    parser.add_argument('-s', '--secondary', help='secondary node', action='store_true')
    parser.add_argument('-i', '--primary_ip', help='ip of the primary node', type=str)
    parser.add_argument('-p', '--primary_port', help='port of the primary node', type=str)
    args = parser.parse_args()
    if args.secondary and (args.primary_ip is None or args.primary_port is None):
        print('usage: __main__.py [-h] [-s] [-i PRIMARY_IP] [-p PRIMARY_PORT] id ip port\n'
              'server.py: error: the following arguments are required: PRIMARY_PORT PRIMARY_PORT ')
        exit(0)
    if args.secondary:
        run_server(args.id, args.ip, args.port, 'secondary', primary_ip=args.primary_ip, primary_port=args.primary_port)
    else:
        run_server(args.id, args.ip, args.port)

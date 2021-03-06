import json
import os
import sys
import time
import threading
from concurrent import futures
import argparse

import grpc

import ChunkServer_pb2
import ChunkServer_pb2_grpc

sys.path.append('../')
sys.path.append('../MasterServer')
from MasterServer import MasterServer_pb2
from MasterServer import MasterServer_pb2_grpc
import settings


class ChunkService(ChunkServer_pb2_grpc.ChunkServerServicer):
    def __init__(self, id, ip, port, master_ip, master_port, role='primary', primary_id=None, primary_ip=None,
                 primary_port=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.role = role
        self.master_ip = master_ip
        self.master_port = master_port
        self.master_status = True
        self.primary_id = primary_id
        self.primary_ip = primary_ip
        self.primary_port = primary_port
        self.secondaries = {}
        self.mates = {}
        self.table = {}  # id:{value:...,type:...}
        self.secondaries_lock = threading.Lock()
        self.table_lock = threading.Lock()
        self.mates_lock = threading.Lock()
        if self.role == 'primary':
            if os.path.exists(settings.Table_File):
                with open(settings.Table_File, 'r') as file:
                    self.table = json.load(file)
            else:
                with grpc.insecure_channel('{}:{}'.format(self.master_ip, self.master_port)) as channel:
                    stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                    response = stub.add_chunk(
                        MasterServer_pb2.Chunk(id=self.id, ip=self.ip, port=self.port, num_keys=len(self.table)))
                    if response.code != 200:
                        print('error: {}'.format(response.msg))
                        r = input('Replace the existed chunk? (y or n)')
                        if r == 'y':
                            response = stub.replace_chunk(
                                MasterServer_pb2.Replace(old_chunk=MasterServer_pb2.Chunk(id=self.id),
                                                         new_chunk=MasterServer_pb2.Chunk(id=self.id, ip=self.ip,
                                                                                          port=self.port,
                                                                                          num_keys=len(self.table))))
                            if response.code != 200:
                                print('add chunk failed, error: {}'.format(response.msg))
                                exit(0)
                        else:
                            exit(0)
        else:
            with grpc.insecure_channel('{}:{}'.format(self.primary_ip, self.primary_port)) as channel:
                stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                response = stub.sync_tables(ChunkServer_pb2.Empty())
                for item in response:
                    self.table[item.key] = {'value': item.value, 'type': item.type}
                response = stub.sync_mates(ChunkServer_pb2.Empty())
                for mate in response:
                    self.mates[mate.id] = {'ip': mate.ip, 'port': mate.port}
                response = stub.add_secondary(ChunkServer_pb2.Secondary(id=self.id, ip=self.ip, port=self.port))
                if response.code != 200:
                    print('error: {}'.format(response.msg))
                    exit(0)

    def heart(self, request, context):
        return ChunkServer_pb2.Reply(msg='I am chunk {}'.format(self.id), code=200)

    def _update_secondary(self, operation, *args, **kwargs):
        for secondary in list(self.secondaries.keys()):
            try:
                with grpc.insecure_channel('{}:{}'.format(self.secondaries[secondary]['ip'],
                                                          self.secondaries[secondary]['port'])) as channel:
                    # print(self.secondaries[secondary])
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    opt = getattr(stub, operation)
                    # response = opt(*args, **kwargs)
                    opt(*args, **kwargs)
                    # print(response.msg, response.code)
            except Exception as e:
                print(e)
                del self.secondaries[secondary]

    def add_mates(self, request, context):
        self.mates_lock.acquire()
        if request.id in self.mates:
            self.mates_lock.release()
            return ChunkServer_pb2.Reply(msg='mate existed', code=400)
        self.mates[request.id] = {'ip': request.ip, 'port': request.port}
        self.mates_lock.release()
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def sync_mates(self, request, context):
        for mate in self.mates:
            yield ChunkServer_pb2.Secondary(id=self.mates['id'], ip=self.mates[mate]['ip'],
                                            port=self.mates[mate]['port'])

    def _select(self):
        primary_id = self.id
        for mate in self.mates:
            with grpc.insecure_channel('{}:{}'.format(self.mates[mate]['ip'], self.mates[mate]['port'])) as channel:
                stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                response = stub.select_primary(ChunkServer_pb2.Secondary(id=self.id, ip=self.ip, port=self.port))
                if response.id != self.id:
                    primary_id = response.id
                    break
        if primary_id == self.id:
            self.role = 'primary'
            for mate in self.mates:
                with grpc.insecure_channel('{}:{}'.format(self.mates[mate]['ip'], self.mates[mate]['port'])) as channel:
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    stub.replace_primary(ChunkServer_pb2.Primary(id=self.id, ip=self.ip, port=self.port))
            with grpc.insecure_channel('{}:{}'.format(self.master_ip, self.master_port)) as channel:
                stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                stub.replace_chunk(
                    MasterServer_pb2.Replace(old_chunk=MasterServer_pb2.Chunk(id=self.primary_id, ip=self.primary_ip,
                                                                              port=self.primary_port),
                                             new_chunk=MasterServer_pb2.Chunk(id=self.id, ip=self.ip, port=self.port,
                                                                              num_keys=len(self.table))))

    def select_primary(self, request, context):
        if int(request.id) > int(self.id):
            return request
        else:
            self._select()
            return ChunkServer_pb2.Secondary(id=self.id, ip=self.ip, port=self.port)

    def replace_primary(self, request, context):
        self.primary_id = request.id
        self.primary_ip = request.ip
        self.primary_port = request.port
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def insert_key(self, request, context):
        if self.role == 'secondary':
            return ChunkServer_pb2.Reply(msg='slave read only', code=403)
        self.table_lock.acquire()
        if request.key in self.table:
            self.table_lock.release()
            return ChunkServer_pb2.Reply(msg='key existed', code=400)
        self.table[request.key] = {'value': request.value, 'type': request.type}
        self._update_secondary('insert_key', request)
        self.table_lock.release()
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def delete_key(self, request, context):
        self.table_lock.acquire()
        if request.key not in self.table:
            self.table_lock.release()
            return ChunkServer_pb2.Reply(msg='key not existed', code=404)
        del self.table[request.key]
        self._update_secondary('delete_key', request)
        self.table_lock.release()
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def update_key(self, request, context):
        if self.role == 'secondary':
            return ChunkServer_pb2.Reply(msg='slave read only', code=403)
        self.table_lock.acquire()
        if request.key not in self.table:
            self.table_lock.release()
            return ChunkServer_pb2.Reply(msg='key not existed', code=404)
        self.table[request.key] = {'value': request.value, 'type': request.type}
        self._update_secondary('update_key', request)
        self.table_lock.release()
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def add_secondary(self, request, context):
        self.secondaries_lock.acquire()
        if request.id in self.secondaries:
            self.secondaries_lock.release()
            return ChunkServer_pb2.Reply(msg='secondary existed', code=400)
        self._update_secondary('add_mates', request)
        self.secondaries[request.id] = {'ip': request.ip, 'port': request.port}
        self.secondaries_lock.release()
        print(self.secondaries)
        return ChunkServer_pb2.Reply(msg='ok', code=200)

    def sync_tables(self, request, context):
        for item in self.table:
            yield ChunkServer_pb2.Value(key=item, value=self.table[item]['value'], type=self.table[item]['type'],
                                        msg='ok', code=200)

    def get_primary(self, request, context):
        return ChunkServer_pb2.Primary(ip=self.primary_ip, port=self.primary_port)

    def get_key(self, request, context):
        if request.key in self.table:
            return ChunkServer_pb2.Value(key=request.key, value=self.table[request.key]['value'],
                                         type=self.table[request.key]['type'], msg='ok', code=200)
        return ChunkServer_pb2.Value(msg='not found', code=404)

    def _persistence(self):
        while True:
            if self.role == 'secondary':  # 主节点不持久化，如果主节点崩溃时，可以从从节点中恢复
                with open(settings.Table_File, 'w') as file:
                    json.dump(self.table, file)
                with open(settings.Info_File, 'w') as file:
                    info = {'id': self.id, 'ip': self.ip, 'port': self.port, 'master_ip': self.master_ip,
                            'master_port': self.master_port, 'role': self.role, 'primary_ip': self.primary_port,
                            'primary_port': self.primary_port}
                    json.dump(info, file)
                # time.sleep(3600)
                time.sleep(settings.Persistence_Time)

    def _detect_heart(self):
        while True:
            for secondary in list(self.secondaries.keys()):
                try:
                    with grpc.insecure_channel('{}:{}'.format(self.secondaries[secondary]['ip'],
                                                              self.secondaries[secondary]['port'])) as channel:
                        stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                        response = stub.heart(ChunkServer_pb2.Empty())
                        if response.code != 200:
                            del self.secondaries[secondary]
                except Exception as e:
                    print(e)
                    del self.secondaries[secondary]
            for mate in list(self.mates.keys()):
                try:
                    with grpc.insecure_channel(
                            '{}:{}'.format(self.mates[mate]['ip'], self.mates[mate]['port'])) as channel:
                        stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                        response = stub.heart(ChunkServer_pb2.Empty())
                        if response.code != 200:
                            del self.mates[mate]
                except Exception as e:
                    print(e)
                    del self.mates[mate]
            try:
                with grpc.insecure_channel('{}:{}'.format(self.master_ip, self.master_port)) as channel:
                    stub = MasterServer_pb2_grpc.MasterServerStub(channel)
                    response = stub.heart(MasterServer_pb2.Empty())
                    if response.code == 200:
                        self.master_status = True
                    else:
                        self.master_status = False
            except Exception as e:
                print(e)
                self.master_status = False
            if self.role != 'primary':
                try:
                    with grpc.insecure_channel('{}:{}'.format(self.primary_ip, self.primary_port)) as channel:
                        stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                        response = stub.heart(ChunkServer_pb2.Empty())
                        if response.code != 200:
                            self._select()
                except Exception as e:
                    print('error: {}'.format(e))
                    self._select()
            time.sleep(settings.Detect_Heart_Time)

    def run(self):
        detect_heart = threading.Thread(target=self._detect_heart)
        detect_heart.setDaemon(True)
        detect_heart.start()
        persistence = threading.Thread(target=self._persistence)
        persistence.setDaemon(True)
        persistence.start()
        persistence.join()
        detect_heart.join()


def run_server(id, ip, port, master_ip, master_port, role='primary', primary_id=None, primary_ip=None,
               primary_port=None):
    chunk = ChunkService(id=id, ip=ip, port=port, master_ip=master_ip, master_port=master_port, role=role,
                         primary_id=primary_id, primary_ip=primary_ip, primary_port=primary_port)
    chunk_run = threading.Thread(target=chunk.run)
    chunk_run.setDaemon(True)
    chunk_run.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ChunkServer_pb2_grpc.add_ChunkServerServicer_to_server(chunk, server)
    server.add_insecure_port('{}:{}'.format(chunk.ip, chunk.port))
    print('Chunk server start')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id', type=str)
    parser.add_argument('ip', help='ip', type=str)
    parser.add_argument('port', help='port', type=str)
    parser.add_argument('master_ip', help='ip of master node', type=str)
    parser.add_argument('master_port', help='port of master node', type=str)
    parser.add_argument('-s', '--secondary', help='secondary node', action='store_true')
    parser.add_argument('-d', '--primary_id', help='id of the primary node', type=str)
    parser.add_argument('-i', '--primary_ip', help='ip of the primary node', type=str)
    parser.add_argument('-p', '--primary_port', help='port of the primary node', type=str)
    args = parser.parse_args()
    if args.secondary and (args.primary_ip is None or args.primary_port is None or args.primary_id is None):
        print('usage: server.py [-h] [-s] [-d PRIMARY_ID] [-i PRIMARY_IP] [-p PRIMARY_PORT]\n'
              '                 id ip port master_ip master_port\n'
              'server.py: error: the following arguments are required: PRIMARY_ID PRIMARY_IP PRIMARY_PORT')
    if args.secondary:
        run_server(args.id, args.ip, args.port, args.master_ip, args.master_port, 'secondary',
                   args.primary_id, args.primary_ip, args.primary_port)
    else:
        run_server(args.id, args.ip, args.port, args.master_ip, args.master_port)

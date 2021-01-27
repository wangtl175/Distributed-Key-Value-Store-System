import sys
import json
import grpc

sys.path.append('../')
sys.path.append('../MasterServer')
sys.path.append('../ChunkServer')
from ChunkServer import ChunkServer_pb2
from ChunkServer import ChunkServer_pb2_grpc
from MasterServer import MasterServer_pb2
from MasterServer import MasterServer_pb2_grpc


class KeyValueClient(object):
    def __init__(self, master_ip, master_port):
        self.master_ip = master_ip
        self.master_port = master_port
        self.master_stub = None

    def connect(self):
        try:
            channel = grpc.insecure_channel('{}:{}'.format(self.master_ip, self.master_port))
            self.master_stub = MasterServer_pb2_grpc.MasterServerStub(channel)
            # print('connect successfully')
        except Exception as e:
            print(e)
            self.master_stub = None

    def put(self, key, value):
        if self.master_stub is not None:
            response = self.master_stub.insert_key(MasterServer_pb2.Key(key=key))
            if response.code == 200:
                # print('connect to chunk {}'.format(response.id))
                with grpc.insecure_channel('{}:{}'.format(response.ip, response.port)) as channel:
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    if type(value) == list or type(value) == dict:
                        v_type = 'json'
                        value = json.dumps(value)
                    else:
                        v_type = str(type(value))
                        value = str(value)
                    response = stub.insert_key(ChunkServer_pb2.Value(key=key, value=value, type=v_type))
                    if response.code != 200:
                        print('error: {}'.format(response.msg))
            else:
                print('error: {}'.format(response.msg))
        else:
            print('put failed: please reconnect')

    def get(self, key):
        if self.master_stub is not None:
            response = self.master_stub.get_chunk(MasterServer_pb2.Key(key=key))
            if response.code == 200:
                # return {'id': response.id, 'ip': response.ip, 'port': response.port}
                # print('connect to chunk {}'.format(response.id))
                with grpc.insecure_channel('{}:{}'.format(response.ip, response.port)) as channel:
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    response = stub.get_key(ChunkServer_pb2.Key(key=key))
                    if response.code == 200:
                        if response.type == 'json':
                            value = json.loads(response.value)
                        elif response.type == "<class 'float'>":
                            value = float(response.value)
                        elif response.type == "<class 'int'>":
                            value = int(response.value)
                        else:
                            value = str(response.value)
                        return value
                    else:
                        print('error: {}'.format(response.msg))
            else:
                print('error: {}'.format(response.msg))
        else:
            print('get failed: please reconnect')

    def delete(self, key):
        if self.master_stub is not None:
            response = self.master_stub.delete_key(MasterServer_pb2.Key(key=key))
            if response.code == 200:
                with grpc.insecure_channel('{}:{}'.format(response.ip, response.port)) as channel:
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    response = stub.delete_key(ChunkServer_pb2.Key(key=key))
                    if response.code != 200:
                        print('error: '.format(response.msg))
            else:
                print('error: {}'.format(response.msg))
        else:
            print('delete failed: please reconnect')

    def update(self, key, value):
        if self.master_stub is not None:
            response = self.master_stub.get_chunk(MasterServer_pb2.Key(key=key))
            if response.code == 200:
                # print('connect to chunk {}'.format(response.id))
                with grpc.insecure_channel('{}:{}'.format(response.ip, response.port)) as channel:
                    stub = ChunkServer_pb2_grpc.ChunkServerStub(channel)
                    if type(value) == list or type(value) == dict:
                        v_type = 'json'
                        value = json.dumps(value)
                    else:
                        v_type = str(type(value))
                        value = str(value)
                    response = stub.update_key(ChunkServer_pb2.Value(key=key, value=value, type=v_type))
                    if response.code != 200:
                        print('error: {}'.format(response.msg))
            else:
                print('error: {}'.format(response.msg))
        else:
            print('update failed: please reconnect')

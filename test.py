import sys

sys.path.append('./ChunkServer')
sys.path.append('./MasterServer')
from Client.client import KeyValueClient

if __name__ == '__main__':
    client = KeyValueClient('127.0.0.1', '5000')
    client.connect()
    client.put('a', 1)
    client.put('b', 2)
    client.put('c', 3)
    a = client.get('a')
    print(a)
    client.update('a', [1, 2, 34])
    a = client.get('a')
    print(a)
    # client.delete('a')

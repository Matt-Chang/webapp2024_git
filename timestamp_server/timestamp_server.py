import sys
import threading
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import datetime
import sys
from django.conf import settings
from .gen_py.timestamp_service import TimestampService


class TimestampServer:
    def getCurrentTimestamp(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

handler = TimestampServer()
processor = TimestampService.Processor(handler)
transport = TSocket.TServerSocket(host='127.0.0.1', port=10000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

def start_server():
    print('Starting the Thrift server...')
    server.serve()
    print('Done.')

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

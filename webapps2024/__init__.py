from threading import Thread
from timestamp_server.timestamp_server import start_server

thrift_server_thread = Thread(target=start_server)
thrift_server_thread.daemon = True
thrift_server_thread.start()

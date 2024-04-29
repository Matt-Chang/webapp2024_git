from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from .gen_py.timestamp_service import TimestampService

def get_timestamp():
    try:
        transport = TSocket.TSocket('127.0.0.1', 10000)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = TimestampService.Client(protocol)

        transport.open()
        timestamp = client.getCurrentTimestamp()
        transport.close()

        return timestamp
    except Thrift.TException as tx:
        print(f'Thrift exception: {tx.message}')
        return None

from django.http import JsonResponse

def current_timestamp(request):
    # Call the get_timestamp function that uses Thrift to fetch the current timestamp
    current_time = get_timestamp()
    if current_time:
        return JsonResponse({'current_time': current_time})
    else:
        # In case of an error, return a default error message or handle as needed
        return JsonResponse({'error': 'Could not fetch the timestamp'}, status=500)

from django.http import JsonResponse, HttpResponseNotFound
from decimal import Decimal
from payapp.convert_points import convert_points
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes

@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def conversion_view(request, currency1, currency2, amount):
    try:
        amount = Decimal(amount)
    except InvalidOperation:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    try:
        converted_amount = convert_points(amount, currency1.upper(), currency2.upper())
        return JsonResponse({
            'converted_amount': str(converted_amount),
            'currency': currency2.upper()
        })
    except KeyError:
        return HttpResponseNotFound('One or both of the provided currencies are not supported.')

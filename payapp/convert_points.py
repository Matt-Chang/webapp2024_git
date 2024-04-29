from decimal import Decimal

def convert_points(amount, from_currency, to_currency):
    conversion_rates = {
        'GBP': {'USD': Decimal('1.3'), 'EUR': Decimal('1.1'), 'GBP': Decimal('1')},
        'USD': {'GBP': Decimal('0.77'), 'EUR': Decimal('0.85'), 'USD': Decimal('1')},
        'EUR': {'GBP': Decimal('0.9'), 'USD': Decimal('1.17'), 'EUR': Decimal('1')},
    }
    rate = conversion_rates[from_currency][to_currency]
    converted_amount = Decimal(amount) * rate
    return converted_amount.quantize(Decimal('0.01'))  # Rounds to two decimal places

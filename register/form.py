from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from decimal import Decimal
from payapp.views import Points

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    points = forms.DecimalField(required=True, initial=Decimal('1000.00'), max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=(('GBP', 'British Pound'), ('USD', 'US Dollar'), ('EUR', 'Euro')))

    class Meta:
        model = User
        fields = ["username", "email", "points", "currency", "password1", "password2"]

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        # Assuming the baseline amount is £1000
        baseline_amount = self.cleaned_data['points']
        currency = self.cleaned_data['currency']
        coverted_amount = convert_currency(baseline_amount, currency)
        print(coverted_amount)
        Points.objects.create(name=user, points=coverted_amount, currency=currency)
        return user
def convert_currency(amount, currency):
    # Dictionary of conversion rates relative to GBP
    conversion_rates = {'GBP': Decimal('1'), 'USD': Decimal('1.3'), 'EUR': Decimal('1.1')}

    # Ensure the amount is a Decimal
    amount_decimal = Decimal(str(amount))

    # Retrieve the conversion rate for the given currency
    conversion_rate_decimal = conversion_rates[currency]

    # Perform the conversion
    converted_amount = amount_decimal * conversion_rate_decimal

    print('Conversion OK')
    return converted_amount
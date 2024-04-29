from django.db import models
from django.contrib.auth.models import User
from .convert_points import convert_points
from decimal import Decimal

class Points(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    currency = models.CharField(max_length=3, default='GBP', choices=(('GBP', 'British Pound'), ('USD', 'US Dollar'), ('EUR', 'Euro')))

    CURRENCY_SYMBOLS = {
        'GBP': '£',
        'USD': '$',
        'EUR': '€',
    }
    def save(self, *args, **kwargs):
        if not self.id:
            if self.currency != 'GBP':
                # Convert 1000 GBP to the instance's currency
                converted_amount = convert_points(1000, 'GBP', self.currency)
                self.points = converted_amount
        super(Points, self).save(*args, **kwargs)

    def formatted_points(self):
        """Return the points with the currency symbol."""
        symbol = self.CURRENCY_SYMBOLS.get(self.currency, '')
        return f"{symbol}{self.points}"

    def __str__(self):
        return f"{self.name} - {self.formatted_points()} points"
# Model to represent the transfer of points between users

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify  # For handling usernames in a consistent case

class PointsTransfer(models.Model):
    sender = models.ForeignKey(User, related_name="sent_transfers", on_delete=models.CASCADE,null=True)  # Sender
    receiver = models.ForeignKey(User, related_name="received_transfers", on_delete=models.CASCADE,null=True)  # Receiver
    money_to_transfer = models.IntegerField()  # Number of points to transfer
    timestamp = models.DateTimeField(auto_now_add=True)

    def currency_symbol(self):
        sender_points = Points.objects.filter(name=self.sender).first()
        if sender_points:
            return Points.CURRENCY_SYMBOLS.get(sender_points.currency, '')
        return ''

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.points_to_transfer} points"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Request money
class PaymentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    )

    sender = models.ForeignKey(User, related_name='sent_payment_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_payment_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment request from {self.sender} to {self.recipient} for {self.amount}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

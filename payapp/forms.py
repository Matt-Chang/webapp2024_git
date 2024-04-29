from django import forms
from django.forms import ModelForm
from .models import PointsTransfer
from .models import PaymentRequest
from django.contrib.auth.models import User

class PointsTransferForm(forms.ModelForm):
    receiver = forms.CharField(max_length=150, label="Receiver Username")

    class Meta:
        model = PointsTransfer
        fields = ['receiver', 'money_to_transfer']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(PointsTransferForm, self).__init__(*args, **kwargs)

    def clean_receiver(self):
        username = self.cleaned_data['receiver']

        if self.user and username == self.user.username:
            raise ValidationError("You cannot transfer money to yourself.")
        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("User does not exist.")
        return receiver

class PaymentRequestForm(forms.ModelForm):
    recipient = forms.CharField(max_length=150, required=True, label="Recipient")

    class Meta:
        model = PaymentRequest
        fields = ['recipient', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(PaymentRequestForm, self).__init__(*args, **kwargs)

    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        if username == self.user.username:
            raise ValidationError("You cannot send a payment request to yourself.")
        try:
            recipient_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("The specified user does not exist.")
        return recipient_user


from django.contrib.auth.forms import UserCreationForm

class AdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            print('saved')
            user.save()
        return user

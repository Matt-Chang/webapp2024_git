from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Points,PointsTransfer,User
from .forms import PointsTransferForm
from django.db.transaction import on_commit
from decimal import Decimal
from .convert_points import convert_points
from .models import PaymentRequest
from .forms import PaymentRequestForm
from django.db import transaction

@transaction.atomic
def points_transfer(request):
    if request.method == 'POST':
        form = PointsTransferForm(request.POST, user=request.user)
        print("y1")
        if form.is_valid():
            print("y2")
            #sender = form.cleaned_data["sender"]
            sender = request.user
            receiver = form.cleaned_data["receiver"]
            points_to_transfer = form.cleaned_data["money_to_transfer"]

            try:
                # Lock the rows for source and destination users
                src_points = Points.objects.select_for_update().get(name__username=sender)
                dst_points = Points.objects.select_for_update().get(name__username=receiver)

                # Convert points to destination user's currency
                converted_points = convert_points(points_to_transfer, src_points.currency, dst_points.currency)
                print(converted_points)
                # Ensure the source user has enough points to transfer
                if src_points.points >= points_to_transfer:
                    # Update points for source user
                    src_points.points -= points_to_transfer
                    src_points.save()

                    # Update points for destination user with converted points
                    dst_points.points += converted_points
                    dst_points.save()
                    print(dst_points)
                    PointsTransfer.objects.create(sender=sender, receiver=receiver, money_to_transfer=points_to_transfer)

                # Use on_commit to inform users after successful transaction
                    transaction.on_commit(lambda: messages.success(request, "Points transferred successfully."))
                else:
                    messages.error(request, "Source user does not have enough points.")
                    return redirect('points_transfer')

            except Points.DoesNotExist:
                messages.error(request, "One or both of the users do not have a points account.")
                return redirect('points_transfer')

            return redirect('show_points', src_username=sender, dst_username=receiver)
        else:
            return render(request, "transactions/pointstransfer.html", {"form": form})
    else:
        form = PointsTransferForm(user=request.user)

    return render(request, "transactions/pointstransfer.html", {"form": form})

@transaction.atomic
def show_points(request, src_username=None, dst_username=None):
    if src_username and dst_username:
        # Fetch the points objects based on the provided usernames
        src_points = get_object_or_404(Points, name__username=src_username)
        dst_points = get_object_or_404(Points, name__username=dst_username)

        return render(request, "transactions/points.html", {"src_points": src_points, "dst_points": dst_points})

    return render(request, "transactions/points.html")

# Request payment
def create_payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST, user=request.user)
        if form.is_valid():
            payment_request = form.save(commit=False)
            payment_request.sender = request.user
            payment_request.status = 'pending'  # Ensure status is set to pending on creation
            payment_request.save()
            return redirect('payment_requests_list')
    else:
        form = PaymentRequestForm(user=request.user)
    return render(request, 'requestpay/create_payment_request.html', {'form': form})


def payment_requests_list(request):
    sent_requests = PaymentRequest.objects.filter(sender=request.user)
    received_requests = PaymentRequest.objects.filter(recipient=request.user)
    return render(request, 'requestpay/payment_requests_list.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })


def make_payment(sender_user, recipient_username, amount):
    """
    Transfer points from one user to another, considering currency conversion.

    Parameters:
    - sender_user: User instance, the user sending the points.
    - recipient_username: str, the username of the recipient user.
    - amount: Decimal, the amount of points to transfer.

    Returns:
    - bool: True if the transfer was successful, False otherwise.
    """
    with transaction.atomic():
        try:
            # Retrieve Points objects for both sender and recipient
            src_points = Points.objects.select_for_update().get(name=sender_user)
            dst_points = Points.objects.select_for_update().get(name__username=recipient_username)

            # Convert points considering currency
            converted_amount = convert_points(amount, src_points.currency, dst_points.currency)

            # Check if sender has enough points
            if src_points.points >= amount:
                src_points.points -= amount  # Deduct from sender
                src_points.save()

                dst_points.points += converted_amount  # Add to recipient
                dst_points.save()

                # Optionally, log this transfer in a PointsTransfer model
                PointsTransfer.objects.create(sender=src_points.name, receiver=dst_points.name, money_to_transfer=amount)

                return True
            else:
                return False  # Insufficient funds
        except Points.DoesNotExist:
            return False  # Sender or recipient does not exist

# Implement a view where users can respond to a payment request.
def respond_to_payment_request(request, request_id, response):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, recipient=request.user)

    if response == 'reject':
        payment_request.status = 'rejected'
        payment_request.save()
    elif response == 'pay':
        success = make_payment(request.user, payment_request.sender, payment_request.amount)
        if success:
            payment_request.status = 'paid'
            payment_request.save()
        else:

            pass

    return redirect('payment_requests_list')


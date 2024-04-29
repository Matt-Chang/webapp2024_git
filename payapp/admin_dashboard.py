from register.form import RegisterForm
from payapp.models import Points,PointsTransfer
from django.shortcuts import render, redirect
from .forms import AdminCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
def admin_dashboard(request):
    if not request.user.is_superuser:
        return render(request, 'transactions/error.html', {'message': 'This dashboard is for administrators only!'})

    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New administrator created successfully!")
            return redirect('admin_dashboard')
    else:
        form = AdminCreationForm()

    users = Points.objects.all()
    transactions = PointsTransfer.objects.select_related('sender', 'receiver').all()

    # Pagination setup
    paginator = Paginator(transactions, 10)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions/admin_dashboard.html', {
        'page_obj': page_obj,
        'users': users,
        'form': form

    })
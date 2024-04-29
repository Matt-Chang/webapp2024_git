"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from register import views as register_views
from payapp import views as transactions_views
from payapp import  admin_dashboard as admin_dashboard_views
from payapp import api as rest_api
from timestamp_server import views as timestamp_server_views
from django.urls import include, path

urlpatterns = [
    path('webapps2024/', include([
        path('admin/', admin.site.urls),
        path("register/", register_views.register_user, name="register"),
        path("login/", register_views.login_user, name="login"),
        path('logout/', register_views.logout_user, name='logout'),
        path('home/', register_views.home, name='home'),
        path('points/', transactions_views.show_points, name='show_points'),
        path('points_transfer/', transactions_views.points_transfer, name='points_transfer'),
        path('show_points/<str:src_username>/<str:dst_username>/', transactions_views.show_points, name='show_points'),
        path('payment-request/create/', transactions_views.create_payment_request, name='create_payment_request'),
        path('payment-requests/', transactions_views.payment_requests_list, name='payment_requests_list'),
        path('payment-request/respond/<int:request_id>/<str:response>/', transactions_views.respond_to_payment_request, name='respond_to_payment_request'),
        path('admin_dashboard/', admin_dashboard_views.admin_dashboard, name='admin_dashboard'),
        path('conversion/<str:currency1>/<str:currency2>/<str:amount>/', rest_api.conversion_view, name='currency_conversion'),
        path('current-timestamp/', timestamp_server_views.current_timestamp, name='current-timestamp'),
    ])),
]

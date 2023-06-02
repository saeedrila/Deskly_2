from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.demo_home, name='demo_home'),
    path('customer-registration/',views.customer_registration, name='customer_registration'),
    path('logout/',views.logout_view, name='logout'),
    path('customer-login/',views.customer_login, name='customer_login'),
    path('',views.home, name='home'),

    path('admin-login',views.admin_login, name='admin_login'),
    path('verify-otp',views.verify_otp, name='verify_otp'),
    path('edit-customer/<int:edit_id>/',views.edit_customer, name='edit_customer'),
    path('admin-dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('customer-dashboard',views.customer_dashboard, name='customer_dashboard'),


    path('ad-template',views.ad_template, name='ad_template'),
    path('ad-edit-template',views.ad_edit_template, name='ad_edit_template'),




#Customer account dashboard
    path('customer-account-dashboard',views.customer_account_dashboard, name='customer_account_dashboard'),
    path('customer-account',views.customer_account, name='customer_account'),
    path('customer-account-edit',views.customer_account_edit, name='customer_account_edit'),
    path('customer-address',views.customer_address, name='customer_address'),
    path('customer-address-add',views.customer_address_add, name='customer_address_add'),
    path('customer-address-edit',views.customer_address_edit, name='customer_address_edit'),
    path('customer-orders',views.customer_orders, name='customer_orders'),
    path('customer-orders-cancel/<int:order_id>',views.customer_orders_cancel, name='customer_orders_cancel'),
]
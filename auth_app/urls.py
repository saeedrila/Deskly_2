from django.urls import path
from . import views

urlpatterns = [
    path('home',views.demo_home, name='demo_home'),
    path('customer-registration/',views.customer_registration, name='customer_registration'),
    path('logout/',views.logout_view, name='logout'),
    path('customer-login/',views.customer_login, name='customer_login'),
    path('',views.home, name='home'),
    path('shop-all',views.shop_all, name='shop_all'),
    path('product-page/<int:product_id>',views.product_page, name='product_page'),
    path('admin-login',views.admin_login, name='admin_login'),
    path('verify-otp',views.verify_otp, name='verify_otp'),
    path('edit-customer/<int:edit_id>/',views.edit_customer, name='edit_customer'),
    path('product-dashboard',views.product_dashboard, name='product_dashboard'),
    path('edit-product/<int:edit_id>',views.edit_product, name='edit_product'),
    


    path('admin-dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('review-dashboard',views.review_dashboard, name='review_dashboard'),
    path('offer-dashboard',views.offer_dashboard, name='offer_dashboard'),
    path('category-dashboard',views.category_dashboard, name='category_dashboard'),
    path('subcategory-dashboard',views.subcategory_dashboard, name='subcategory_dashboard'),
    path('banner-dashboard',views.banner_dashboard, name='banner_dashboard'),
    path('customer-dashboard',views.customer_dashboard, name='customer_dashboard'),


    path('ad-template',views.ad_template, name='ad_template'),
    path('ad-edit-template',views.ad_edit_template, name='ad_edit_template'),


    path('customer-account-dashboard',views.customer_account_dashboard, name='customer_account_dashboard'),
    path('customer-account',views.customer_account, name='customer_account'),
    path('customer-account-edit',views.customer_account_edit, name='customer_account_edit'),
    path('customer-address',views.customer_address, name='customer_address'),
    path('customer-address-add',views.customer_address_add, name='customer_address_add'),
    path('customer-address-edit',views.customer_address_edit, name='customer_address_edit'),
    path('customer-orders',views.customer_orders, name='customer_orders'),
    path('customer-orders-cancel/<int:order_id>',views.customer_orders_cancel, name='customer_orders_cancel'),

]
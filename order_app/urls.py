from django.urls import path
from . import views

urlpatterns = [
    path('cart',views.cart, name='cart'),
    path('wish-list',views.wish_list, name='wish_list'),
    path('order-dashboard',views.order_dashboard, name='order_dashboard'),
    path('order-edit/<int:order_id>/',views.order_edit, name='order_edit'),
    path("cancel-order/", views.cancel_order, name="cancel_order"),
    path('coupon-dashboard',views.coupon_dashboard, name='coupon_dashboard'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wish-list/<int:product_id>/', views.add_to_wish_list, name='add_to_wish_list'),
    path('remove-from-wish-list/<int:product_id>/', views.remove_from_wish_list, name='remove_from_wish_list'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('get-wishlist-count/', views.get_wishlist_count, name='get_wishlist_count'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('checkout-address/', views.checkout_address, name='checkout_address'),
    path('checkout-payment/<int:address_id>/', views.checkout_payment, name='checkout_payment'),


    path('deskly-razorpay/<int:address_id>/', views.deskly_razorpay, name='deskly_razorpay'),
    path('razorpay-demo', views.razorpay_demo, name='razorpay_demo'),
    path('success', views.success, name='success'),

]
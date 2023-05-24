from django.urls import path
from . import views

urlpatterns = [
    path('cart',views.cart, name='cart'),
    path('wish-list',views.wish_list, name='wish_list'),
    path('order-dashboard',views.order_dashboard, name='order_dashboard'),
    path('coupon-dashboard',views.coupon_dashboard, name='coupon_dashboard'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wish-list/<int:product_id>/', views.add_to_wish_list, name='add_to_wish_list'),
    path('remove-from-wish-list/<int:product_id>/', views.remove_from_wish_list, name='remove_from_wish_list'),
    path('get-wishlist-count/', views.get_wishlist_count, name='get_wishlist_count'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
]
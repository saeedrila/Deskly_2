from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("wish-list", views.wish_list, name="wish_list"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "add-to-wish-list/<int:product_id>/",
        views.add_to_wish_list,
        name="add_to_wish_list",
    ),
    path(
        "remove-from-wish-list/<int:product_id>/",
        views.remove_from_wish_list,
        name="remove_from_wish_list",
    ),
    path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("update-cart/<int:product_id>/", views.update_cart, name="update_cart"),
    path("check-stock/<int:product_id>/", views.check_stock, name="check_stock"),
    path("get-wishlist-count/", views.get_wishlist_count, name="get_wishlist_count"),
    path("get-cart-count/", views.get_cart_count, name="get_cart_count"),
    # Order
    path("order-dashboard", views.order_dashboard, name="order_dashboard"),
    path("order-edit/<int:order_id>/", views.order_edit, name="order_edit"),
    path("cancel-order/", views.cancel_order, name="cancel_order"),
    # Coupon
    path("coupon-dashboard", views.coupon_dashboard, name="coupon_dashboard"),
    path("coupon-add", views.coupon_add, name="coupon_add"),
    path("coupon-edit/<int:coupon_id>/", views.coupon_edit, name="coupon_edit"),
    path("verify-coupon/", views.verify_coupon, name="verify_coupon"),
    path("render-cart-totals/", views.render_cart_totals, name="render_cart_totals"),
    # Offer
    path("banner-dashboard", views.banner_dashboard, name="banner_dashboard"),
    path("offer-dashboard", views.offer_dashboard, name="offer_dashboard"),
    path("offer-add", views.offer_add, name="offer_add"),
    path("offer-edit/<int:offer_id>/", views.offer_edit, name="offer_edit"),
    path("thank-you/", views.thank_you, name="thank_you"),
    path("checkout-address/", views.checkout_address, name="checkout_address"),
    path(
        "checkout-payment/<int:address_id>/",
        views.checkout_payment,
        name="checkout_payment",
    ),
    # Test paths
    path(
        "deskly-razorpay/<int:address_id>/",
        views.deskly_razorpay,
        name="deskly_razorpay",
    ),
    path("razorpay-demo", views.razorpay_demo, name="razorpay_demo"),
    path("success", views.success, name="success"),
]

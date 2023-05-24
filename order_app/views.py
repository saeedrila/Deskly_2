from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal

from product_app.models import *
from . models import *

# Create your views here.

# Cart and add to cart need modification
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user).order_by('id')

    for item in cart_items:
        item.subtotal = Decimal(item.product.mrp) * item.quantity
    
    total = sum((Decimal(item.subtotal) for item in cart_items))
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    cart_item, created = CartItem.objects.get_or_create(customer=request.user, product=product)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({'message': 'Product quantity updated in cart.'}, status=200)

import json
def update_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, customer=request.user)
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'message': 'Invalid quantity.'}, status=400)
    
    if quantity < 1:
        return JsonResponse({'message': 'Quantity must be at least 1.'}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'message': 'Cart item updated.'}, status=200)

def remove_from_cart(request, product_id):
    # User authentication not added
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    cart_item = CartItem.objects.filter(customer=request.user, product=product)
    if not cart_item.exists():
        return JsonResponse({'message': 'Product is not in your cart.'}, status=400)

    cart_item.delete()

    return JsonResponse({'message': 'Product removed from cart.'}, status=200)



def wish_list(request):
    wish_list_items = WishList.objects.filter(customer=request.user)
    context = {
        'wish_list_items': wish_list_items,
    }
    return render(request, 'wish_list.html', context)

def add_to_wish_list(request, product_id):
    # User authentication not added
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    wishlist_item_exists = WishList.objects.filter(customer=request.user, product=product).exists()
    if wishlist_item_exists:
        return JsonResponse({'message': 'Product is already in your wishlist.'}, status=400)

    wishlist_item = WishList(customer=request.user, product=product)
    wishlist_item.save()

    return JsonResponse({'message': 'Product added to wishlist.'}, status=200)

def remove_from_wish_list(request, product_id):
    # User authentication not added
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    wishlist_item = WishList.objects.filter(customer=request.user, product=product)
    if not wishlist_item.exists():
        return JsonResponse({'message': 'Product is not in your wishlist.'}, status=400)

    wishlist_item.delete()

    return JsonResponse({'message': 'Product removed from wishlist.'}, status=200)

def get_wishlist_count(request):
    count = WishList.objects.filter(customer=request.user).count()
    return JsonResponse({'count': count})

def get_cart_count(request):
    count = CartItem.objects.filter(customer=request.user).count()
    return JsonResponse({'count': count})

# @never_cache
def order_dashboard(request):
    # if request.session.get('is_admin'):
        context = {
            'reviews': Product.objects.order_by('-id'),
        }
        return render(request, "order_dashboard.html", context)
    # else:
    #     return redirect("admin_login")

# @never_cache
def order_edit(request, order_id):
    # if request.session.get('is_admin'):
        context = {
            'orders': Order.objects.order_by('-id'),
        }
        return render(request, "order_edit.html", context)
    # else:
    #     return redirect("admin_login")



def edit_customer(request, edit_id):
    if request.session.get('is_admin'):
        customer = Account.objects.get(id=edit_id)
        if request.POST:
            customer.is_active = bool(request.POST.get('is_active'))
            customer.save()
            return redirect("customer_dashboard")
        context = {
            'customer': customer,
        }
        return render(request, "edit_customer.html", context)
    else:
        return redirect('admin_login')



# @never_cache
def coupon_dashboard(request):
    # if request.session.get('is_admin'):
        context = {
            'reviews': Product.objects.order_by('-id'),
        }
        return render(request, "coupon_dashboard.html", context)
    # else:
    #     return redirect("admin_login")



# Codes from Afif
# @never_cache
# def cart(request):
#     user = request.user
#     cart_items = Cart.objects.filter(user=user)
    
#     cart_items = cart_items.annotate(item_total=F('quantity') * F('product__price'))
    
    
#     subtotal   = cart_items.aggregate(subtotal=Sum('item_total'))['subtotal']

   
#     for cart_item in cart_items:
#         cart_item.total_price = cart_item.item_total
#         cart_item.save()
#     shipping_cost = 10 
    
#     total = subtotal + shipping_cost if subtotal else 0
    
#     context = {
#         'cart_items': cart_items,
#         'subtotal'  : subtotal,
#         'total'     : total,
#     }
#     return render(request, 'cart.html', context)


# @never_cache
# def add_to_cart(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return redirect('product_not_found')

#     quantity = request.POST.get('quantity')

#     if not quantity:
#         quantity = 1

#     cart, created = Cart.objects.get_or_create(
#         product=product,
#         user=request.user,
#         defaults={'quantity': 0}
#     )

#     cart.quantity += quantity
#     cart.save()

#     return redirect('cart')

# @never_cache
# def remove_from_cart(request, cart_item_id):
#     try:
#         cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
#         cart_item.delete()
#     except Cart.DoesNotExist:
#         pass
    
#     return redirect('cart')


# @never_cache
# def checkout(request):
#     user = request.user
#     cart_items = Cart.objects.filter(user=user)
    
#     cart_items = cart_items.annotate(item_total=F('quantity') * F('product__price'))
    
#     subtotal = cart_items.aggregate(subtotal=Sum('item_total'))['subtotal']

#     shipping_cost = 10 
    
#     total = subtotal + shipping_cost if subtotal else 0
    
#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'total': total,
#     }
#     return render(request, 'checkout.html', context)
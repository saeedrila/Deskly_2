from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import razorpay

from product_app.models import *
from . models import *
from . forms import PaymentForm


# Cart and add to cart need modification
def cart(request):
    if not request.user.is_authenticated:
        return redirect("home")
    cart_items = CartItem.objects.filter(customer=request.user).order_by('id')

    for item in cart_items:
        item.subtotal = Decimal(item.product.mrp) * item.quantity
    
    total = sum((Decimal(item.subtotal) for item in cart_items))
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

@never_cache
def checkout_address(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        if selected_address_id:
            address = Address.objects.get(id=selected_address_id)
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            address1 = request.POST.get('address1')
            customer = request.user
            address = Address.objects.create(customer=customer, name=name, email=email, line_1=address1)
        return redirect('checkout_payment', address_id=address.id)
    else:
        cart_items = CartItem.objects.filter(customer=request.user).order_by('id')
        for item in cart_items:
            item.subtotal = Decimal(item.product.mrp) * item.quantity
        total = sum((Decimal(item.subtotal) for item in cart_items))
        
        addresses = Address.objects.filter(customer=request.user).order_by('-id')

        context = {
            'cart_items': cart_items,
            'total': total,
            'addresses': addresses
        }
        return render(request, "checkout_address.html", context)

@never_cache
def deskly_razorpay(request, order_id=1):
    try:
        order = Order.objects.get(id=order_id)
    except:
        messages.error(request, "Order not found")
    context = {
        'order': order
    }
    return render(request, "razorpay_demo.html", context)

@never_cache
def checkout_payment(request, address_id=1):
    cart_items = CartItem.objects.filter(customer=request.user).order_by('id')
    total = sum(Decimal(item.product.mrp) * item.quantity for item in cart_items)
    shipping = 0
    net_total = total + shipping
    print('**********')
    print(net_total)
    print('**********')
    for item in cart_items:
        item.subtotal = Decimal(item.product.mrp) * item.quantity
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_option = form.cleaned_data['payment_option']
            if payment_option in ['cod', 'razorpay']:
                for item in cart_items:
                    product = item.product
                    quantity = item.quantity
                    subtotal = Decimal(product.mrp) * quantity
                    net_total = subtotal

                    order = Order(
                        customer=request.user,
                        address=address,
                        product=product,
                        quantity=quantity,
                        payment=payment_option,
                        date=now(),
                        status='Pending',
                        net_total=net_total,
                    )
                    order.save()

                cart_items.delete()

                if payment_option == 'cod':
                    return redirect('thank_you')
                else:
                    try:
                        # Razorpay
                        amount = int(net_total) * 100
                        client = razorpay.Client(auth =("rzp_test_WGlv594z1DLEPO","rSzkwzdBivOZmQK0xu4q3UeD"))
                        payment = client.order.create ({'amount' : amount, 'currency': 'INR', 'payment_capture': '1'})

                        print('********** Razorpay Integration **********')
                        print(payment)
                        print('*******************************************')

                        if 'id' in payment:
                            order.razorpay_order_id = payment['id']
                            order.save()
                            context = {
                                'cart': order,
                                'net_total': net_total,
                                'payment': payment
                            }
                            messages.success(request, "Razorpay payment initiated")
                            return render(request, 'deskly_razorpay.html', context)
                        else:
                            messages.error(request, "Error creating Razorpay order: {}".format(payment.get('error')))
                    except Exception as e:
                        print('********** Razorpay Integration Error **********')
                        print('Error:', e)
                        print('***********************************************')
                        messages.error(request, "Error during Razorpay integration: {}".format(str(e)))
            else:
                messages.error(request, "The selected payment option is not available now. Please choose another option.")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        form = PaymentForm()
        form.request = request

    context = {
        'cart_items': cart_items,
        'total': total,
        'net_total': net_total,
        'form': form,
        'address': address,
    }
    return render(request, "checkout_payment.html", context)

@never_cache
@csrf_exempt
def thank_you(request):
    if request.method =="POST":
        a = request.POST
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        print('***********')
        print(a)
        print('***********')
        print(order_id)
        order = Order.objects.get(razorpay_order_id = order_id)
        order.razorpay_paid = True
        order.razorpay_payment_id = a['razorpay_payment_id']
        order.razorpay_payment_signature = a['razorpay_signature']
        order.save()
        messages.success(request, order_id)
        return render(request, "thank_you.html")
    return render(request, "thank_you.html")


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
    if not request.user.is_authenticated:
        return redirect("home")
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

@never_cache
def order_dashboard(request):
    if request.session.get('is_admin'):
        search_query = request.GET.get('search')
        orders = Order.objects.order_by('-id')

        if search_query:
            orders = orders.filter(
                Q(customer__username__icontains=search_query) |
                Q(product__name__icontains=search_query) |
                Q(payment__icontains=search_query) |
                Q(address__line_1__icontains=search_query)
            )
        per_page = int(request.GET.get('entries', 5))
        paginator = Paginator(orders, per_page)  # Change the number of items per page as needed
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'messages': messages.get_messages(request),
            'orders': page,  # Pass the paginated page object to the template
        }
        return render(request, "order_dashboard.html", context)
    else:
        return redirect("admin_login")


@never_cache
def order_edit(request, order_id=17):
    if request.session.get('is_admin'):
        order = Order.objects.get(id=order_id)
        if request.POST:
            order.admin_action = bool(request.POST.get('admin_action'))          
            order.status = request.POST.get('status')
            order.save()
            return redirect("order_dashboard")

        context = {
            'order': Order.objects.get(id=order_id),
        }
        return render(request, "order_edit.html", context)
    else:
        return redirect("admin_login")
    
from django.http import JsonResponse

def cancel_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        # Perform the necessary operations to update the order status
        try:
            order = Order.objects.get(id=order_id)
            order.admin_action = False
            order.save()
            return JsonResponse({"status": "success"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

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

# Test methods
def razorpay_demo(request):
    if request.method == "POST":
        name = request. POST .get ("name")
        amount = int(request.POST. get ("amount")) * 100
        client = razorpay.Client(auth =("rzp_test_WGlv594z1DLEPO","rSzkwzdBivOZmQK0xu4q3UeD"))
        payment = client.order.create ({'amount' : amount, 'currency': 'INR', 'payment_capture': '1'})
        print(payment)
        purchase = RazorpayDemo(name = name , amount=amount, payment_id = payment ['id' ])
        purchase.save()
        context = {
            'payment': payment
        }
        return render(request, "razorpay_demo.html", context)
    
    context={}
    return render(request, "razorpay_demo.html", context)

@csrf_exempt
def success(request):
    if request.method =="POST":
        a = request.POST
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        print('***********')
        print(a)
        print('***********')
        print(order_id)
        order = RazorpayDemo.objects.get(payment_id = order_id)
        order.paid = True
        order.save()
    return render(request, "success.html")
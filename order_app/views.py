from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import Http404,JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from decimal import Decimal
from django.contrib.auth.models import AnonymousUser
import razorpay

from product_app.models import *
from . models import *
from . forms import PaymentForm
from product_app.views import *



def verify_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        try:
            coupon = Coupon.objects.get(Q(coupon_code__iexact=coupon_code))
            if coupon.is_active:
                request.session['coupon_code'] = coupon.coupon_code
                message = 'Coupon code is valid'
            else:
                message = 'Invalid coupon code'
        except Coupon.DoesNotExist:
            message = 'Invalid coupon code'
        return HttpResponse(message)

def render_cart_totals(request):
    context = {
    }
    return render(request, 'cart_totals.html', context)

@never_cache
def checkout_address(request):
    if not request.user.is_authenticated:
        return redirect('customer_registration')
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
            try:
                product = Product.objects.get(id=item.product_id)
                category_id = product.category_id
                category_offers = CategoryOffer.objects.filter(category_id=category_id)[:1]

                if product.offer_is_active or category_offers.exists():
                    if product.offer_is_active:
                        product_retail_price = round(product.mrp * (1 - product.offer_percentage / 100))
                    else:
                        product_retail_price = product.mrp

                    if category_offers.exists():
                        category_offer = category_offers[0]
                        discount_percentage = category_offer.discount_percentage
                        offer_product_price = round(product_retail_price * (1 - discount_percentage / 100))
                        product.offer_product_price = offer_product_price
                        item.offer_product_price = offer_product_price
                else:
                    pass
            except Product.DoesNotExist:
                pass
            try:
                item.subtotal = Decimal(item.offer_product_price) * item.quantity
            except:
                item.subtotal = Decimal(item.product.mrp) * item.quantity
        total = sum((Decimal(item.subtotal) for item in cart_items))
        discount_percentage = 0
        coupon_code = request.session.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(Q(coupon_code__iexact=coupon_code))
                if coupon.is_active:
                    discount_percentage = coupon.discount_percentage
            except Coupon.DoesNotExist:
                pass

        coupon_discount = round(total * Decimal(discount_percentage/100))
        net_total = total - coupon_discount
        addresses = Address.objects.filter(customer=request.user).order_by('-id')

        context = {
            'cart_items': cart_items,
            'total': total,
            'addresses': addresses,
            'coupon_discount': coupon_discount,
            'net_total': net_total,
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
    for item in cart_items:
        try:
            product = Product.objects.get(id=item.product_id)
            category_id = product.category_id
            category_offers = CategoryOffer.objects.filter(category_id=category_id)[:1]

            if product.offer_is_active or category_offers.exists():
                if product.offer_is_active:
                    product_retail_price = round(product.mrp * (1 - product.offer_percentage / 100))
                else:
                    product_retail_price = product.mrp

                if category_offers.exists():
                    category_offer = category_offers[0]
                    discount_percentage = category_offer.discount_percentage
                    offer_product_price = round(product_retail_price * (1 - discount_percentage / 100))
                    product.offer_product_price = offer_product_price
                    item.offer_product_price = offer_product_price
            else:
                pass
        except Product.DoesNotExist:
            pass
        try:
            item.subtotal = Decimal(item.offer_product_price) * item.quantity
        except:
            item.subtotal = Decimal(item.product.mrp) * item.quantity
    total = sum((Decimal(item.subtotal) for item in cart_items))
    shipping = 0
    discount_percentage = 0
    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(Q(coupon_code__iexact=coupon_code))
            if coupon.is_active:
                discount_percentage = coupon.discount_percentage
        except Coupon.DoesNotExist:
            pass

    coupon_discount = round(total * Decimal(discount_percentage/100))
    net_total = total + shipping - coupon_discount
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
                order = Order(
                    customer=request.user,
                    address=address,
                    payment=payment_option,
                    date=now(),
                    status='Pending',
                    net_total=0,
                )
                order.save()
                net_total = 0

                for item in cart_items:
                    product = item.product
                    quantity = item.quantity
                    subtotal = Decimal(product.mrp) * quantity
                    net_total += subtotal

                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_item.save()
                    product.stock -= quantity
                    product.sell_count += quantity
                    product.save()
                #Coupon discount on net_total
                discount_percentage = 0
                coupon_code = request.session.get('coupon_code')
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(Q(coupon_code__iexact=coupon_code))
                        if coupon.is_active:
                            discount_percentage = coupon.discount_percentage
                    except Coupon.DoesNotExist:
                        pass

                coupon_discount = round(total * Decimal(discount_percentage/100))
                net_total = total - coupon_discount

                order.net_total = net_total
                order.save()

                cart_items.delete()
                #delete coupon from session
                try:
                    del request.session['coupon_code']
                except:
                    pass
                if payment_option == 'cod':
                    return redirect('thank_you')
                else:
                    try:
                        # Razorpay
                        amount = int(net_total) * 100
                        client = razorpay.Client(auth =(settings.RAZORPAY_KEY,settings.RAZORPAY_SECRET))
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
        'coupon_discount': coupon_discount,
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

#Cart related methods
def cart(request):
    if not request.user.is_authenticated:
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return redirect("home")
        
        cart_items = CartItem.objects.filter(device=device_id).order_by('id')
    else:
        cart_items = CartItem.objects.filter(customer=request.user).order_by('id')

    for item in cart_items:
        try:
            product = Product.objects.get(id=item.product_id)
            category_id = product.category_id
            category_offers = CategoryOffer.objects.filter(category_id=category_id)[:1]

            if product.offer_is_active or category_offers.exists():
                if product.offer_is_active:
                    product_retail_price = round(product.mrp * (1 - product.offer_percentage / 100))
                else:
                    product_retail_price = product.mrp

                if category_offers.exists():
                    category_offer = category_offers[0]
                    discount_percentage = category_offer.discount_percentage
                    offer_product_price = round(product_retail_price * (1 - discount_percentage / 100))
                    product.offer_product_price = offer_product_price
                    item.offer_product_price = offer_product_price
            else:
                item.offer_product_price = None

        except Product.DoesNotExist:
            pass

        try:
            item.subtotal = Decimal(item.offer_product_price) * item.quantity
        except:
            item.subtotal = Decimal(item.product.mrp) * item.quantity

    total = sum((Decimal(item.subtotal) for item in cart_items))

    discount_percentage = 0
    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code)
            if coupon.is_active:
                discount_percentage = coupon.discount_percentage
        except Coupon.DoesNotExist:
            pass

    coupon_discount = round(total * Decimal(discount_percentage / 100))
    net_total = total - coupon_discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'coupon_discount': coupon_discount,
        'net_total': net_total,
    }

    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'message': 'Device ID not found.'}, status=400)

        cart_item, created = CartItem.objects.get_or_create(device=device_id, product=product)
    else:
        cart_item, created = CartItem.objects.get_or_create(customer=request.user, product=product)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({'message': 'Product quantity updated in cart.'}, status=200)

def update_cart(request, product_id):
    if not request.user.is_authenticated:
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'message': 'Device ID not found.'}, status=400)

        cart_item = get_object_or_404(CartItem, product_id=product_id, device=device_id)
    else:
        cart_item = get_object_or_404(CartItem, product_id=product_id, customer=request.user)
    
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'message': 'Invalid quantity.'}, status=400)

    if quantity < 1:
        return JsonResponse({'message': 'Quantity must be at least 1.'}, status=400)

    product = cart_item.product
    if product.stock < quantity:
        return JsonResponse({'message': 'Only limited stock available.'}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'message': 'Cart item updated.'}, status=200)


def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'message': 'Device ID not found.'}, status=400)

        cart_item = CartItem.objects.filter(device=device_id, product_id=product_id)
    else:
        cart_item = CartItem.objects.filter(customer=request.user, product_id=product_id)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    if not cart_item.exists():
        return JsonResponse({'message': 'Product is not in your cart.'}, status=400)

    cart_item.delete()

    return JsonResponse({'message': 'Product removed from cart.'}, status=200)


def get_cart_count(request):
    if not request.user.is_authenticated:
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'count': 0})
        
        count = CartItem.objects.filter(device=device_id).count()
    else:
        count = CartItem.objects.filter(customer=request.user).count()

    return JsonResponse({'count': count})


#Stock availability check
def check_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_available = product.stock
    return JsonResponse({'stock': stock_available})
#This is a sample line

#Wishlist related methods
def wish_list(request):
    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return redirect("home")

        wish_list_items = WishList.objects.filter(device=device_id)
    else:
        wish_list_items = WishList.objects.filter(customer=request.user)

    context = {
        'wish_list_items': wish_list_items,
    }
    return render(request, 'wish_list.html', context)

def add_to_wish_list(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'message': 'Device ID not found.'}, status=400)

        wishlist_item_exists = WishList.objects.filter(device=device_id, product=product).exists()
        if wishlist_item_exists:
            return JsonResponse({'message': 'Product is already in your wishlist.'}, status=400)

        wishlist_item = WishList(device=device_id, product=product)
        wishlist_item.save()

        return JsonResponse({'message': 'Product added to wishlist.'}, status=200)
    else:
        wishlist_item_exists = WishList.objects.filter(customer=request.user, product=product).exists()
        if wishlist_item_exists:
            return JsonResponse({'message': 'Product is already in your wishlist.'}, status=400)

        wishlist_item = WishList(customer=request.user, product=product)
        wishlist_item.save()

        return JsonResponse({'message': 'Product added to wishlist.'}, status=200)

def remove_from_wish_list(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product does not exist.'}, status=404)

    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'message': 'Device ID not found.'}, status=400)

        wishlist_item = WishList.objects.filter(device=device_id, product=product)
    else:
        wishlist_item = WishList.objects.filter(customer=request.user, product=product)

    if not wishlist_item.exists():
        return JsonResponse({'message': 'Product is not in your wishlist.'}, status=400)

    wishlist_item.delete()

    return JsonResponse({'message': 'Product removed from wishlist.'}, status=200)

def get_wishlist_count(request):
    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get('device_id')
        if not device_id:
            return JsonResponse({'count': 0})
        
        count = WishList.objects.filter(device=device_id).count()
    else:
        count = WishList.objects.filter(customer=request.user).count()

    return JsonResponse({'count': count})


@never_cache
def order_dashboard(request):
    if request.session.get('is_admin'):
        search_query = request.GET.get('search')
        per_page = int(request.GET.get('entries', 5))
        orders = Order.objects.order_by('-id')

        if search_query:
            orders = orders.filter(
                Q(customer__username__icontains=search_query) |
                Q(orderitem__product__name__icontains=search_query) |
                Q(payment__icontains=search_query) |
                Q(address__line_1__icontains=search_query)
            )

        paginator = Paginator(orders, per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            'messages': messages.get_messages(request),
            'orders': page,
            'order_items': OrderItem.objects.select_related('product').filter(order__in=page),
            'search_query': search_query,
            'per_page': per_page,
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



@never_cache
def coupon_dashboard(request):
    # if request.session.get('is_admin'):
        context = {
            'coupons': Coupon.objects.order_by('-id'),
        }
        return render(request, "coupon_dashboard.html", context)
    # else:
    #     return redirect("admin_login")

#Coupon add modal method
def coupon_add(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        discount_percentage = request.POST.get("discount_percentage")
        issued_quantity = request.POST.get("issued_quantity")
        remaining_quantity = request.POST.get("remaining_quantity")
        coupon = Coupon(coupon_code = coupon_code, discount_percentage = discount_percentage, 
                issued_quantity = issued_quantity, remaining_quantity = remaining_quantity)
        coupon.save()
        messages.success(request, "Coupon successfully added")
        return redirect(coupon_dashboard)
    messages.error(request, "Coupon could not be added")
    return redirect(coupon_dashboard)

def coupon_edit(request, coupon_id):
    if request.method == "POST":
        coupon = Coupon.objects.get(id = coupon_id)
        is_active = request.POST.get("is_active")
        if is_active:
            messages.success("Coupon has been activated successfully")
        else:
            messages.success("Coupon has been dectivated successfully")
        coupon.is_active = is_active
        coupon.save()
        return redirect(coupon_dashboard)
    return redirect(coupon_dashboard)

@never_cache
def banner_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'reviews': Product.objects.order_by('-id'),
        }
        return render(request, "banner_dashboard.html", context)
    else:
        return redirect("admin_login")

@never_cache
def offer_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'offers': CategoryOffer.objects.order_by('-id'),
            'categories': Category.objects.order_by('-id'),
        }
        return render(request, "offer_dashboard.html", context)
    else:
        return redirect("admin_login")

def offer_edit(request, offer_id):
    pass

#Category offer add modal method
def offer_add(request):

    if request.method == "POST":
        category_id = request.POST.get("category")
        category = get_object_or_404(Category, id=category_id)
        discount_percentage = request.POST.get("discount_percentage")
        offer = CategoryOffer(category = category, discount_percentage = discount_percentage)
        offer.save()

        messages.success(request, "Category offer successfully added")
        return redirect(category_dashboard)
    messages.error(request, "Coupon could not be added")
    return redirect(category_dashboard)



# Test methods
def razorpay_demo(request):
    if request.method == "POST":
        name = request. POST .get ("name")
        amount = int(request.POST. get ("amount")) * 100
        client = razorpay.Client(auth =(settings.RAZORPAY_KEY,settings.RAZORPAY_SECRET))
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

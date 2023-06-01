from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import secrets
import smtplib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from django.views.decorators.cache import never_cache
import time
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator

from . forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from . models import *
from product_app.models import *
from product_app.forms import *
from . forms import *
from order_app.models import *


def demo_home(request):
    context = {}
    context['some_string'] = 'This is some string I am passing from views.py'
    return render(request, "demo_home.html", context)

def home(request):
    context = {}
    context['popular_products'] = Product.objects.order_by('-sell_count')[:3]
    context['categories'] = Category.objects.all()[:6]
    context['latest_products'] = Product.objects.order_by('-date_added')[:6]
    
    return render(request, "home.html", context)

def customer_registration(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            generated_otp = generate_otp()
            sender_email = "rilasaeed@gmail.com"
            receiver_email = email
            password = "gcofjtizzuokqhkm"

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, generated_otp)

            except smtplib.SMTPAuthenticationError:
                messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                return redirect('signup')

            login(request, account)
            request.session['email'] = email
            request.session['otp'] = generated_otp
            return redirect('verify_otp')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def verify_otp(request):
    if request.method == "POST":
        customer = Account.objects.get(email=request.session['email'])
        server_gernerated_otp = request.session.get('otp')
        customer_input_otp = request.POST['otp']
        if server_gernerated_otp == customer_input_otp:
            customer.is_verified = True
            customer.save()
            del request.session['email']
            del request.session['otp']
            return redirect('home')
        else:
            customer.delete()
            return redirect('customer_registration')
    return render(request,'verify_otp.html')

def generate_otp(length = 6):
    return ''.join(secrets.choice("0123456789") for i in range(length)) 

def logout_view(request):
    logout(request)
    del request.session
    return redirect('home')

def customer_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect ('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect('home')

    form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'login.html', context)

def customer_account_dashboard(request):
    user = request.user
    if user.is_authenticated:
        account = request.user
        context = {
            'account': account,
        }
        return render(request, "customer_account_dashboard.html", context)
    else:
        return redirect ('home')

def customer_account(request):
    user = request.user
    if user.is_authenticated:
        account = request.user
        context = {
            'account': account,
        }
        return render(request, "customer_account.html", context)
    else:
        return redirect ('home')
    
def customer_account_edit(request):
    user = request.user
    if user.is_authenticated:
        account = request.user
        context = {
            'account': account,
        }
        return render(request, "customer_account_edit.html", context)
    else:
        return redirect ('home')

def customer_address(request):
    customer_addresses = Address.objects.filter(customer=request.user)
    context = {
        'customer_addresses': customer_addresses,
    }
    return render(request, "customer_address.html", context)


def customer_address_add(request):
    user = request.user
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        line_1 = request.POST['line_1']

        address = Address()
        address.customer = user
        address.name = name
        address.email = email
        address.line_1 = line_1
        address.save()
        return redirect(customer_address)

    context = {}
    return render(request, "customer_address_add.html", context)

def customer_address_edit(request, address_id):
    user = request.user
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        line_1 = request.POST['line_1']

        address = Address()
        address.customer = user
        address.name = name
        address.email = email
        address.line_1 = line_1
        address.save()
        return redirect(customer_address)

    context = {}
    return render(request, "customer_address_add.html", context)

def customer_orders(request):
    customer_orders = Order.objects.filter(customer=request.user).order_by('-id')
    context = {
        'orders': customer_orders,
    }
    return render(request, "customer_orders.html", context)

def customer_orders_cancel(request, order_id):
    order_id = order_id
    customer_orders = Order.objects.filter(customer=request.user)
    context = {
        'orders': customer_orders,
    }
    return render(request, "customer_orders_cancel.html", context)



def shop_all(request):
    context = {}
    try:
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
    except Product.DoesNotExist:
        raise Http404("Product does not exist.")
    return render(request, "shop_all.html", context)

def product_page(request, product_id=None):
    context = {}
    try:
        context['product'] = Product.objects.get(id = product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist.")
    return render(request, "product_page.html", context)


def admin_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect ('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user is not None and user.is_admin:
                login(request, user)
                customer = Account.objects.filter(email = email).first()
                if customer:
                    request.session['is_admin'] = customer.is_admin
                print(request.session['is_admin'])
                return redirect('admin_dashboard')
    form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "admin_login.html", context)

@never_cache
def admin_dashboard(request):
    if request.session.get('is_admin'):
        context = {}
        context = {
            'recent_orders': range(6),
            'recent_products_added': Product.objects.order_by('-id')[:6],
        }
        context['some_string'] = 'This is some string I am passing from views.py'
        return render(request, "admin_dashboard.html", context)
    else:
        return redirect('admin_login')

@never_cache
def customer_dashboard(request):
    if request.session.get('is_admin'):
        customers = Account.objects.order_by('-id')
        paginator = Paginator(customers, 4)  # Change the number of items per page as needed
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'messages': messages.get_messages(request),
            'customers': page,  # Pass the paginated page object to the template
        }
        return render(request, "customer_dashboard.html", context)
    else:
        return redirect('admin_login')

@never_cache
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
def product_dashboard(request):
    if request.session.get('is_admin'):
        products = Product.objects.order_by('-id')
        paginator = Paginator(products, 4)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'messages': messages.get_messages(request),
            'products': page, 
        }
        return render(request, "product_dashboard.html", context)
    else:
        return redirect('admin_login')

@never_cache
def edit_product(request, edit_id=None):
    if request.session.get('is_admin'):
        product_obj = Product.objects.get(id=edit_id)
        if request.POST:
            product_obj.name = request.POST.get('name')
            brand_id = request.POST.get('brand')
            category_id = request.POST.get('category_id')
            sub_category_id = request.POST.get('sub_category_id')
            try:
                brand_obj = Brand.objects.get(id=brand_id)
                product_obj.brand = brand_obj
            except Brand.DoesNotExist:
                pass
            try:
                category_obj = Category.objects.get(id=category_id)
                product_obj.category = category_obj
            except Category.DoesNotExist:
                pass
            try:
                sub_category_obj = Subcategory.objects.get(id=sub_category_id)
                product_obj.sub_category_id = sub_category_obj
            except Subcategory.DoesNotExist:
                pass
            product_obj.mrp = request.POST.get('mrp')
            product_obj.availability = bool(request.POST.get('availability'))
            product_obj.stock = request.POST.get('stock')
            product_obj.sell_count = request.POST.get('sell_count')
            product_obj.save()
            messages.success(request, 'Product successfully edited.')
            return redirect("product_dashboard")
        context = {
            'product': product_obj,
        }
        return render(request, "edit_product.html", context)
    else:
        return redirect('admin_login')

@never_cache
def review_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'reviews': Product.objects.order_by('-id'),
        }
        return render(request, "review_dashboard.html", context)
    else:
        return redirect("admin_login")

@never_cache
def category_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'categories': Category.objects.order_by('id'),
        }
        return render(request, "category_dashboard.html", context)
    else:
        return redirect("admin_login")




@never_cache
def subcategory_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'subcategories': Subcategory.objects.order_by('-id'),
        }
        return render(request, "subcategory_dashboard.html", context)
    else:
        return redirect("admin_login")



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
            'offers': Product.objects.order_by('-id'),
        }
        return render(request, "offer_dashboard.html", context)
    else:
        return redirect("admin_login")



def ad_template(request):
    context = {}
    context['some_string'] = 'This is some string I am passing from views.py'
    return render(request, "ad_template.html", context)

def ad_edit_template(request):
    context = {}
    context['some_string'] = 'This is some string I am passing from views.py'
    return render(request, "ad_edit_template.html", context)
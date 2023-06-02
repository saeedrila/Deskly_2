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
    if request.user.is_authenticated:
        customer_orders = Order.objects.filter(customer=request.user).order_by('-id')[:5]
        latest_order = Order.objects.filter(customer=request.user).order_by('-id')[:1]
        order_count = Order.objects.filter(customer=request.user).count()
        labels = []
        data = []
        for order in customer_orders:
            labels.append(order.id)
            data.append(order.net_total)
        account = request.user
        context = {
            'account': account,
            'labels': labels,
            'data': data,
            'latest_order': latest_order,
            'order_count': order_count,
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
    if 'messages' in request.session:
        messages.success(request, request.session.pop('messages'))
    context = {
        'orders': customer_orders,
    }
    return render(request, "customer_orders.html", context)

def customer_orders_cancel(request, order_id):
    if request.POST:
        admin_action = request.POST['admin_action_value']
        order = Order.objects.get(id=order_id)
        order.admin_action = admin_action
        order.save()
        messages.success(request, "Order successfully cancelled")
        return redirect("customer_orders")
    order = Order.objects.get(id=order_id)
    context = {
        'order': order,
    }
    return render(request, "customer_orders_cancel.html", context)



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
        orders = Order.objects.order_by('-id')[:5]
        recent_products_added = Product.objects.order_by('-id')[:6]
        labels = []
        data = []
        for order in orders:
            labels.append(order.id)
            data.append(order.net_total)
        context = {
            'recent_orders': range(6),
            'recent_products_added': recent_products_added,
            'labels': labels,
            'data': data,
        }
        return render(request, "admin_dashboard.html", context)
    else:
        return redirect('admin_login')

@never_cache
def customer_dashboard(request):
    if request.session.get('is_admin'):
        customers = Account.objects.order_by('-id')
        paginator = Paginator(customers, 4)
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





def ad_template(request):
    context = {}
    context['some_string'] = 'This is some string I am passing from views.py'
    return render(request, "ad_template.html", context)

def ad_edit_template(request):
    context = {}
    context['some_string'] = 'This is some string I am passing from views.py'
    return render(request, "ad_edit_template.html", context)
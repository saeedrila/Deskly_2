from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import secrets
import smtplib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from django.views.decorators.cache import never_cache
import time
from django.http import Http404

from . forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from . models import *
from product_app.models import *
from product_app.forms import *


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

def customer_account(request):
    context = {}
    context['popular_products'] = Product.objects.order_by('-sell_count')[:3]
    context['categories'] = Category.objects.all()[:6]
    context['latest_products'] = Product.objects.order_by('-date_added')[:6]
    
    return render(request, "customer_account.html", context)

def shop_all(request):
    context = {}
    try:
        context['products'] = Product.objects.all()
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
        context = {
            'customers': Account.objects.order_by('-id'),
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
        context = {
            'messages': messages.get_messages(request),
            'products': Product.objects.order_by('-id'), 
        }
        time.sleep(2)
        print(request)
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
def add_product(request):
    if request.session.get('is_admin'):
        if request.POST:
            product_obj = Product()
            product_obj.name = request.POST.get('name')
            product_obj.description = request.POST.get('description')
            brand_id = request.POST.get('brand')
            category_id = request.POST.get('category_id')
            sub_category_id = request.POST.get('sub_category_id')
            try:
                brand_obj = Brand.objects.get(id=brand_id)
                product_obj.brand_id = brand_obj
            except Brand.DoesNotExist:
                pass
            try:
                category_obj = Category.objects.get(id=category_id)
                product_obj.category_id = category_obj
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
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                filename = default_storage.save('products/' + image_file.name, ContentFile(image_file.read()))
                product_obj.image = filename

            product_obj.save()
            messages.success(request, 'Product successfully added.')
            return redirect("product_dashboard")
        context = {}
        return render(request, "add_product.html", context)
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


# Category Model Form views
from .forms import *
from django.http import JsonResponse

def category_model_form(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            return redirect('success')
    else:
        product_form = ProductForm()
        context = {
            'product_form': product_form,
        }
        print(product_form)
        return render(request, 'category_model_form.html', context)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    subcategories_list = list(subcategories)  # Convert queryset to list
    context = {
        'subcategories': subcategories_list,
    }
    print(context)
    return JsonResponse(context, safe=False)



@never_cache
def subcategory_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'reviews': Product.objects.order_by('-id'),
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
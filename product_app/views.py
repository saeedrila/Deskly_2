from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.paginator import Paginator


from . forms import *

def search_demo(request):
    return render(request, 'search_demo.html')

def get_names(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Names.objects.filter(name__icontains=search)
        for obj in objs:
            payload.append({
                'name': obj.name
            })
    return JsonResponse(payload, safe=False)



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


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            return redirect('product_dashboard')
    else:
        product_form = ProductForm()
    context = {
        'product_form': product_form,
    }
    return render(request, "add_product.html", context)

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


#Dependent drop down menu
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    subcategories_list = list(subcategories)  # Convert queryset to list
    context = {
        'subcategories': subcategories_list,
    }
    print(context)
    return JsonResponse(context, safe=False)


#Sample methods
def example_form(request):
    example_form_instance = ExampleForm()
    context = {
        'example_form_instance' : example_form_instance
    }
    return render(request, 'example_form.html', context)

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
        return render(request, 'category_model_form.html', context)
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.storage import default_storage
import uuid


from .forms import *
from order_app.models import *


def shop_all(request):
    query = request.GET.get('search')
    selected_categories = request.GET.getlist('category[]')

    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query))
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    if not products.exists():
        raise Http404("No products found.")

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'selected_categories': selected_categories
    }

    device_id = request.COOKIES.get('device_id')
    if not device_id:
        device_id = uuid.uuid4()
    
    response = render(request, "shop_all.html", context)
    response.set_cookie('device_id', device_id)
    return response



def product_page(request, product_id=None):
    context = {}
    try:
        product = Product.objects.get(id=product_id)

        if product.offer_is_active:
            product_retail_price = round(product.mrp * (1 - product.offer_percentage / 100))
            context['product_offer'] = product.offer_percentage
        else:
            product_retail_price = product.mrp

        category_id = product.category_id
        category_offers = CategoryOffer.objects.filter(category_id=category_id)[:1]
        if category_offers.exists():
            category_offer = category_offers[0]
            discount_percentage = category_offer.discount_percentage
            offer_product_price = round(product_retail_price * (1 - discount_percentage / 100))
            product.offer_product_price = offer_product_price
            print("Category offer exists")
        else:
            print("No category offer found")
        context['product'] = product

    except Product.DoesNotExist:
        return render(request, '404.html')

    except Product.DoesNotExist:
        raise Http404("Product does not exist.")
    
    device_id = request.COOKIES.get('device_id')
    if not device_id:
        device_id = uuid.uuid4()
        response = render(request, "shop_all.html", context)
        response.set_cookie('device_id', device_id)
        return response
    
    return render(request, "product_page.html", context)


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            image_files = request.FILES.getlist('image_files')
            for image_file in image_files:
                image = ProductImage.objects.create(product=product, image=image_file)
                image.image.save(image_file.name, image_file)  # Save the image using Django's ImageField
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
        search_query = request.GET.get('search')
        products = Product.objects.order_by('-id')
        if products.exists():
            first_product = products.first()
            print("*****************************")
            print(first_product.name)
            print(first_product.brand.name)
            for image in first_product.images.all():
                print(image.image.url)
            print("*****************************")
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        per_page = int(request.GET.get('entries', 5))
        paginator = Paginator(products, per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'messages': messages.get_messages(request),
            'products': page,
            'first_product': first_product,  # Pass the first product to the context
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
    
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category_image = request.FILES.get('category_image')
        category = Category(name=category_name, description=category_description)

        filename = default_storage.get_available_name(category_image.name)
        path = default_storage.save(filename, category_image)

        category.image = path
        category.save()
        messages.success(request, 'New category has been created successfully.')
        return redirect('category_dashboard')
    return redirect('category_dashboard')


@never_cache
def subcategory_dashboard(request):
    if request.session.get('is_admin'):
        context = {
            'subcategories': Subcategory.objects.order_by('-id'),
        }
        return render(request, "subcategory_dashboard.html", context)
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
    
#Search demo not working
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

#Working
def search_jquery(request):
    return render(request, 'search_jquery.html')

def get_suggestion(request):
    print(request)
    request_query = request.GET.get('term')
    queryset = Product.objects.filter(name__icontains=request_query)
    my_list = []
    my_list += [x.name for x in queryset]
    return JsonResponse(my_list, safe=False)

# Image crop example
def image_crop(request):
    form = ImageForm()
    context = {'form': form}
    return render(request, 'image_crop.html', context)
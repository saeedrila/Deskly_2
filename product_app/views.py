from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
import uuid

from .forms import *
from order_app.models import *


def shop_all(request):
    query = request.GET.get("search")
    selected_categories = request.GET.getlist("category[]")

    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query))
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "selected_categories": selected_categories,
    }

    device_id = request.COOKIES.get("device_id")
    if not device_id:
        device_id = uuid.uuid4()

    response = render(request, "shop_all.html", context)
    response.set_cookie("device_id", device_id)
    return response


def product_page(request, product_id=None):
    context = {}
    try:
        product = Product.objects.get(id=product_id)

        if product.offer_is_active:
            product_retail_price = round(
                product.mrp * (1 - product.offer_percentage / 100)
            )
            product.offer_product_price = product_retail_price
            context["product_offer"] = product.offer_percentage
        else:
            product_retail_price = product.mrp

        category_offers = CategoryOffer.objects.filter(category_id=product.category_id)[
            :1
        ]
        if category_offers.exists():
            category_offer = category_offers[0]
            discount_percentage = category_offer.discount_percentage
            offer_product_price = round(
                product_retail_price * (1 - discount_percentage / 100)
            )
            product.offer_product_price = offer_product_price
            print("Category offer exists")
        else:
            print("No category offer found")

        context = {"product": product}

    except Product.DoesNotExist:
        raise Http404("Product does not exist.")

    device_id = request.COOKIES.get("device_id")
    if not device_id:
        device_id = uuid.uuid4()
        response = render(request, "shop_all.html", context)
        response.set_cookie(
            "device_id", device_id, max_age=604800
        )  # Set max_age to 1 week (604800 seconds)
        return response

    return render(request, "product_page.html", context)


def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            image_files = request.FILES.getlist("image_files")
            for image_file in image_files:
                image = ProductImage.objects.create(product=product, image=image_file)
                image.image.save(
                    image_file.name, image_file
                )  # Save the image using Django's ImageField
            return redirect("product_dashboard")
    else:
        product_form = ProductForm()
    context = {
        "product_form": product_form,
    }
    return render(request, "add_product.html", context)


@never_cache
def product_dashboard(request):
    if request.session.get("is_admin"):
        search_query = request.GET.get("search")
        products = Product.objects.order_by("-id")
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
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        per_page = int(request.GET.get("entries", 5))
        paginator = Paginator(products, per_page)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        context = {
            "messages": messages.get_messages(request),
            "products": page,
            "first_product": first_product,  # Pass the first product to the context
        }
        return render(request, "product_dashboard.html", context)
    else:
        return redirect("admin_login")


@never_cache
def edit_product(request, edit_id=None):
    if request.session.get("is_admin"):
        product_obj = Product.objects.get(id=edit_id)
        if request.POST:
            product_obj.name = request.POST.get("name")[:50]
            brand_id = request.POST.get("brand")
            category_id = request.POST.get("category_id")
            sub_category_id = request.POST.get("sub_category_id")
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
            product_obj.mrp = request.POST.get("mrp")
            product_obj.availability = request.POST.get("availability")
            product_obj.stock = request.POST.get("stock")
            product_obj.sell_count = request.POST.get("sell_count")
            product_obj.save()
            messages.success(request, "Product successfully edited.")
            return redirect("product_dashboard")
        context = {
            "product": product_obj,
        }
        return render(request, "edit_product.html", context)
    else:
        return redirect("admin_login")


# Review dashboard (Not using at the moment)
@never_cache
def review_dashboard(request):
    if request.session.get("is_admin"):
        context = {
            "reviews": Product.objects.order_by("-id"),
        }
        return render(request, "review_dashboard.html", context)
    else:
        return redirect("admin_login")


# Brand related functions(Need editing)
@never_cache
def brand_dashboard(request):
    if request.session.get("is_admin"):
        context = {
            "brands": Brand.objects.order_by("-is_active", "id"),
        }
        return render(request, "brand_dashboard.html", context)
    else:
        return redirect("admin_login")


def add_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get("brand_name")
        brand_description = request.POST.get("brand_description")
        brand_image = request.FILES.get("brand_image")
        brand = Brand(name=brand_name, description=brand_description)

        filename = default_storage.get_available_name(brand_image.name)
        path = default_storage.save(filename, brand_image)

        brand.image = path
        brand.save()
        messages.success(request, "New brand has been created successfully.")
        return redirect("brand_dashboard")
    return redirect("brand_dashboard")


def edit_brand(request):
    if request.session.get("is_admin"):
        if request.POST:
            brand_id = request.POST.get("brand_id")
            brand_name = request.POST.get("brand_name")
            brand_description = request.POST.get("brand_description")
            brand_is_active = request.POST.get("brand_is_active")
            print("Enters edit brand")
            print(brand_id)

            brand_obj = get_object_or_404(Brand, id=brand_id)
            brand_obj.name = brand_name
            brand_obj.description = brand_description
            brand_obj.is_active = brand_is_active
            brand_obj.save()
            messages.success(request, "Brand successfully edited.")
            print("brand detials succesfully changed")
            return redirect("brand_dashboard")
    else:
        return redirect("admin_login")


# Ajax brand data fetching for edit modal
def get_brand_data(request):
    brand_id = request.GET.get("brandId")
    try:
        brand = Brand.objects.get(id=brand_id)
        data = {
            "name": brand.name,
            "description": brand.description,
            "is_active": brand.is_active,
            "image_url": brand.image.url if brand.image else None,
            # Add any additional fields you want to include in the response
        }
        return JsonResponse(data)
    except Brand.DoesNotExist:
        return JsonResponse({"error": "Brand not found"}, status=404)


# Category related functions
@never_cache
def category_dashboard(request):
    if request.session.get("is_admin"):
        context = {
            "categories": Category.objects.order_by("-is_active", "id"),
        }
        return render(request, "category_dashboard.html", context)
    else:
        return redirect("admin_login")


def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_description = request.POST.get("category_description")
        category_image = request.FILES.get("category_image")
        category = Category(name=category_name, description=category_description)

        filename = default_storage.get_available_name(category_image.name)
        path = default_storage.save(filename, category_image)

        category.image = path
        category.save()
        messages.success(request, "New category has been created successfully.")
        return redirect("category_dashboard")
    return redirect("category_dashboard")


def edit_category(request):
    if request.session.get("is_admin"):
        if request.POST:
            category_id = request.POST.get("category_id")
            category_name = request.POST.get("category_name")
            category_description = request.POST.get("category_description")
            category_is_active = request.POST.get("category_is_active")
            print("Enters edit category")

            try:
                category_obj = Category.objects.get(id=category_id)
                category_obj.name = category_name
                category_obj.description = category_description
                category_obj.is_active = category_is_active
                category_obj.save()
                messages.success(request, "Category successfully edited.")
                print("category detials succesfully changed")
                return redirect("category_dashboard")
            except Category.DoesNotExist:
                return redirect("category_dashboard")
    else:
        return redirect("admin_login")


# Ajax category data fetching for edit modal of category
def get_category_data(request):
    category_id = request.GET.get("categoryId")
    try:
        category = Category.objects.get(id=category_id)
        data = {
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
            "image_url": category.image.url if category.image else None,
        }
        return JsonResponse(data)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)


# Subcategory related functions
@never_cache
def subcategory_dashboard(request):
    if request.session.get("is_admin"):
        context = {
            "subcategories": Subcategory.objects.order_by("-id"),
            "categories": Category.objects.order_by("-id"),
        }
        return render(request, "subcategory_dashboard.html", context)
    else:
        return redirect("admin_login")


def add_subcategory(request):
    if request.method == "POST":
        subcategory_name = request.POST.get("subcategory_name")
        subcategory_description = request.POST.get("subcategory_description")
        subcategory_image = request.FILES.get("subcategory_image")
        category_id = request.POST.get("category_id")
        subcategory = Subcategory(
            name=subcategory_name,
            description=subcategory_description,
            category_id=category_id,
        )

        filename = default_storage.get_available_name(subcategory_image.name)
        path = default_storage.save(filename, subcategory_image)

        subcategory.image = path
        subcategory.save()
        messages.success(request, "New subcategory has been created successfully.")
        return redirect("subcategory_dashboard")
    return redirect("subcategory_dashboard")


def edit_subcategory(request):
    if request.session.get("is_admin"):
        if request.POST:
            subcategory_id = request.POST.get("subcategory_id")
            subcategory_name = request.POST.get("subcategory_name")
            subcategory_description = request.POST.get("subcategory_description")
            subcategory_is_active = request.POST.get("subcategory_is_active")
            print("Enters edit subcategory")

            try:
                subcategory_obj = Subcategory.objects.get(id=subcategory_id)
                subcategory_obj.name = subcategory_name
                subcategory_obj.description = subcategory_description
                subcategory_obj.is_active = subcategory_is_active
                subcategory_obj.save()
                messages.success(request, "Subcategory successfully edited.")
                print("subcategory detials succesfully changed")
                return redirect("subcategory_dashboard")
            except Subcategory.DoesNotExist:
                return redirect("subcategory_dashboard")
    else:
        return redirect("admin_login")


# Ajax subcategory data fetching for edit modal
def get_subcategory_data(request):
    subcategory_id = request.GET.get("subcategoryId")
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        data = {
            "name": subcategory.name,
            "category_name": subcategory.category.name,
            "description": subcategory.description,
            "is_active": subcategory.is_active,
            "image_url": subcategory.image.url if subcategory.image else None,
            # Add any additional fields you want to include in the response
        }
        return JsonResponse(data)
    except Subcategory.DoesNotExist:
        return JsonResponse({"error": "Subcategory not found"}, status=404)


# Dependent drop down menu for category and subcategory
def get_subcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = Subcategory.objects.filter(category_id=category_id).values(
        "id", "name"
    )
    subcategories_list = list(subcategories)  # Convert queryset to list
    context = {
        "subcategories": subcategories_list,
    }
    print(context)
    return JsonResponse(context, safe=False)


# Sample methods
def example_form(request):
    example_form_instance = ExampleForm()
    context = {"example_form_instance": example_form_instance}
    return render(request, "example_form.html", context)


def category_model_form(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            return redirect("success")
    else:
        product_form = ProductForm()
        context = {
            "product_form": product_form,
        }
        return render(request, "category_model_form.html", context)


# Search demo not working
def search_demo(request):
    return render(request, "search_demo.html")


def get_names(request):
    search = request.GET.get("search")
    payload = []
    if search:
        objs = Names.objects.filter(name__icontains=search)
        for obj in objs:
            payload.append({"name": obj.name})
    return JsonResponse(payload, safe=False)


# Working
def search_jquery(request):
    return render(request, "search_jquery.html")


def get_suggestion(request):
    print(request)
    request_query = request.GET.get("term")
    queryset = Product.objects.filter(name__icontains=request_query)
    my_list = []
    my_list += [x.name for x in queryset]
    return JsonResponse(my_list, safe=False)


# Image crop example
def image_crop(request):
    form = ImageForm()
    context = {"form": form}
    return render(request, "image_crop.html", context)

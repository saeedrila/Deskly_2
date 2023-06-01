from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse

from . forms import *

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
    
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    subcategories_list = list(subcategories)  # Convert queryset to list
    context = {
        'subcategories': subcategories_list,
    }
    print(context)
    return JsonResponse(context, safe=False)
from django.urls import path
from . import views

urlpatterns = [
    path('add-product',views.add_product, name='add_product'),



    #Sample pages
    path('example-form/', views.example_form, name='example_form'),
    path('category-model-form/', views.category_model_form, name='category_model_form'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),

]

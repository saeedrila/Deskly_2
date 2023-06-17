from django.urls import path
from . import views

urlpatterns = [
    path('add-product',views.add_product, name='add_product'),
    path('add-category',views.add_category, name='add_category'),

    path('shop-all/',views.shop_all, name='shop_all'),
    path('product-page/<int:product_id>',views.product_page, name='product_page'),
    path('product-dashboard',views.product_dashboard, name='product_dashboard'),
    path('edit-product/<int:edit_id>',views.edit_product, name='edit_product'),
    path('review-dashboard',views.review_dashboard, name='review_dashboard'),
    path('category-dashboard',views.category_dashboard, name='category_dashboard'),
    path('subcategory-dashboard',views.subcategory_dashboard, name='subcategory_dashboard'),





#Sample pages
    #Image crop example
    path('image-crop/', views.image_crop, name='image_crop'),

    #Search using jquery
    path('search-jquery', views.search_jquery, name='search_jquery'),
    path('get-suggestion', views.get_suggestion, name='get_suggestion'),

    #Search demo
    path('search-demo', views.search_demo, name='search_demo'),
    path('get-names/', views.get_names, name='get_names'),

    path('example-form/', views.example_form, name='example_form'),
    path('category-model-form/', views.category_model_form, name='category_model_form'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
]

from django.urls import path
from . import views

urlpatterns = [
#Product
    path('add-product',views.add_product, name='add_product'),
    path('edit-product/<int:edit_id>',views.edit_product, name='edit_product'),
    path('product-page/<int:product_id>',views.product_page, name='product_page'),
    path('product-dashboard',views.product_dashboard, name='product_dashboard'),
    path('shop-all/',views.shop_all, name='shop_all'),

#Brand
    path('brand-dashboard',views.brand_dashboard, name='brand_dashboard'),
    path('add-brand/',views.add_brand, name='add_brand'),
    path('edit-brand/',views.edit_brand, name='edit_brand'),
    path('get-brand-data/', views.get_brand_data, name='get_brand_data'),

#Category
    path('category-dashboard',views.category_dashboard, name='category_dashboard'),
    path('add-category/',views.add_category, name='add_category'),
    path('edit-category/',views.edit_category, name='edit_category'),
    path('get-category-data/', views.get_category_data, name='get_category_data'),

#Subcategory
    path('subcategory-dashboard/',views.subcategory_dashboard, name='subcategory_dashboard'),
    path('add-subcategory/',views.add_subcategory, name='add_subcategory'),
    path('edit-subcategory/',views.edit_subcategory, name='edit_subcategory'),
    path('get-subcategory-data/', views.get_subcategory_data, name='get_subcategory_data'),
    #Used for dependent dropdown
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),




#Review
    path('review-dashboard',views.review_dashboard, name='review_dashboard'),

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
]
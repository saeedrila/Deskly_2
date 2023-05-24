from django.urls import path
from . import views

urlpatterns = [
    path('example/', views.example_view, name='example'),
    # Add more URL patterns here
]

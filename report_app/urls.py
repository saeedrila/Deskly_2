from django.urls import path
from . import views

urlpatterns = [
    path('report-pdf-order/', views.report_pdf_order, name='report_pdf_order'),


# PDF Report generator
    path('report-generator/', views.report_generator, name='report_generator'),

#Chart generator
    path('chart-demo/', views.chart_demo, name='chart_demo'),

#Sample pages
    path('example-form/', views.example_form, name='example_form'),
]
from django.urls import path
from . import views

urlpatterns = [
#Report
    path('report-pdf-order/', views.report_pdf_order, name='report_pdf_order'),

#Chart generator
    path('chart-demo/', views.chart_demo, name='chart_demo'),
    path('chart-customer-dashboard-order/', views.chart_customer_dashboard_order, name='chart_customer_dashboard_order'),

# PDF Report generator Demo
    path('report-generator/', views.report_generator, name='report_generator'),
#Sample pages
    path('example-form/', views.example_form, name='example_form'),
]
from django.urls import path
from . import views

app_name = 'financials'

urlpatterns = [
    path('', views.financial_dashboard, name='dashboard'),
    path('payments/', views.payment_list, name='payments'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('invoices/', views.invoice_list, name='invoices'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('reports/', views.financial_reports, name='reports'),
    path('expenses/', views.expense_list, name='expenses'),
    path('payroll/', views.payroll_list, name='payroll'),
]

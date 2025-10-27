from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TuitionFeeViewSet, PaymentViewSet, PlacementFeeViewSet, PayrollViewSet, ExpenseViewSet, InvoiceViewSet, FinancialReportViewSet

router = DefaultRouter()
router.register(r'tuition-fees', TuitionFeeViewSet, basename='tuitionfee')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'placement-fees', PlacementFeeViewSet, basename='placementfee')
router.register(r'payroll', PayrollViewSet, basename='payroll')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'reports', FinancialReportViewSet, basename='financialreport')

urlpatterns = [
    path('', include(router.urls)),
]

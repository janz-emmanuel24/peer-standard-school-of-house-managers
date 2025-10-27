from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count
from .models import TuitionFee, Payment, PlacementFee, Payroll, Expense, Invoice, FinancialReport
from .serializers import (
    TuitionFeeSerializer, PaymentSerializer, PlacementFeeSerializer,
    PayrollSerializer, ExpenseSerializer, InvoiceSerializer, FinancialReportSerializer
)


class TuitionFeeViewSet(viewsets.ModelViewSet):
    """Tuition fee viewset"""
    queryset = TuitionFee.objects.filter(is_active=True)
    serializer_class = TuitionFeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify tuition fees
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment viewset"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Payment.objects.all()
        elif hasattr(user, 'student_profile'):
            return Payment.objects.filter(student=user.student_profile)
        else:
            return Payment.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify payments
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark payment as completed"""
        payment = self.get_object()
        payment.status = 'completed'
        payment.save()
        
        return Response({'status': 'paid'})


class PlacementFeeViewSet(viewsets.ModelViewSet):
    """Placement fee viewset"""
    queryset = PlacementFee.objects.all()
    serializer_class = PlacementFeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return PlacementFee.objects.all()
        elif hasattr(user, 'employer_profile'):
            return PlacementFee.objects.filter(employer=user.employer_profile)
        else:
            return PlacementFee.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify placement fees
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PayrollViewSet(viewsets.ModelViewSet):
    """Payroll viewset"""
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Payroll.objects.all()
        else:
            return Payroll.objects.filter(employee=user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify payroll
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """Expense viewset"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify expenses
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, approved_by=self.request.user)


class InvoiceViewSet(viewsets.ModelViewSet):
    """Invoice viewset"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify invoices
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FinancialReportViewSet(viewsets.ModelViewSet):
    """Financial report viewset"""
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Only admin can modify reports
            if not self.request.user.user_type == 'admin':
                permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get financial summary"""
        if request.user.user_type != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Calculate financial summary
        total_revenue = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        pending_payments = Payment.objects.filter(status='pending').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        overdue_invoices = Invoice.objects.filter(
            status__in=['sent', 'pending'],
            due_date__lt=timezone.now().date()
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        summary = {
            'total_revenue': total_revenue,
            'pending_payments': pending_payments,
            'total_expenses': total_expenses,
            'net_profit': total_revenue - total_expenses,
            'overdue_invoices': overdue_invoices,
            'profit_margin': 0
        }
        
        if total_revenue > 0:
            summary['profit_margin'] = round((summary['net_profit'] / total_revenue) * 100, 2)
        
        return Response(summary)

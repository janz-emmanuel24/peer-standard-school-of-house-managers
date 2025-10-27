from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Payment, Invoice, Expense, Payroll


@login_required
def financial_dashboard(request):
    """Financial dashboard (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view financial data.')
        return redirect('dashboard:home')
    
    # Financial summary
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    pending_payments = Payment.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    recent_payments = Payment.objects.select_related('student__user').order_by('-payment_date')[:10]
    recent_expenses = Expense.objects.order_by('-expense_date')[:10]
    
    return render(request, 'financials/dashboard.html', {
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'total_expenses': total_expenses,
        'recent_payments': recent_payments,
        'recent_expenses': recent_expenses
    })


@login_required
def payment_list(request):
    """List all payments"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view payments.')
        return redirect('dashboard:home')
    
    payments = Payment.objects.select_related('student__user').order_by('-payment_date')
    return render(request, 'financials/payments.html', {'payments': payments})


@login_required
def payment_create(request):
    """Create new payment"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to create payments.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        # Create payment logic here
        messages.success(request, 'Payment created successfully!')
        return redirect('financials:payments')
    
    return render(request, 'financials/payment_create.html')


@login_required
def invoice_list(request):
    """List all invoices"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view invoices.')
        return redirect('dashboard:home')
    
    invoices = Invoice.objects.order_by('-issue_date')
    return render(request, 'financials/invoices.html', {'invoices': invoices})


@login_required
def invoice_create(request):
    """Create new invoice"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to create invoices.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        # Create invoice logic here
        messages.success(request, 'Invoice created successfully!')
        return redirect('financials:invoices')
    
    return render(request, 'financials/invoice_create.html')


@login_required
def financial_reports(request):
    """Financial reports"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view reports.')
        return redirect('dashboard:home')
    
    return render(request, 'financials/reports.html')


@login_required
def expense_list(request):
    """List all expenses"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view expenses.')
        return redirect('dashboard:home')
    
    expenses = Expense.objects.order_by('-expense_date')
    return render(request, 'financials/expenses.html', {'expenses': expenses})


@login_required
def payroll_list(request):
    """List payroll records"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to view payroll.')
        return redirect('dashboard:home')
    
    payroll_records = Payroll.objects.select_related('employee').order_by('-pay_date')
    return render(request, 'financials/payroll.html', {'payroll_records': payroll_records})
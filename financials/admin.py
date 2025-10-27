from django.contrib import admin
from .models import TuitionFee, Payment, PlacementFee, Payroll, Expense, Invoice, FinancialReport


@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    """Tuition Fee admin"""
    list_display = ('course', 'amount', 'effective_date', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'effective_date', 'expiry_date')
    search_fields = ('course__title', 'description')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment admin"""
    list_display = ('student', 'payment_type', 'amount', 'payment_method', 'status', 'payment_date', 'processed_by')
    list_filter = ('payment_type', 'payment_method', 'status', 'payment_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'reference_number')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('student', 'enrollment', 'payment_type', 'amount', 'payment_method', 'status')
        }),
        ('Transaction Information', {
            'fields': ('payment_date', 'reference_number', 'description', 'receipt_file')
        }),
        ('Processing', {
            'fields': ('processed_by', 'created_at')
        }),
    )


@admin.register(PlacementFee)
class PlacementFeeAdmin(admin.ModelAdmin):
    """Placement Fee admin"""
    list_display = ('employer', 'student', 'amount', 'fee_type', 'due_date', 'paid_date', 'status')
    list_filter = ('fee_type', 'status', 'due_date', 'paid_date')
    search_fields = ('employer__company_name', 'student__user__first_name', 'student__user__last_name', 'reference_number')
    readonly_fields = ('created_at',)


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    """Payroll admin"""
    list_display = ('employee', 'payroll_type', 'amount', 'pay_period_start', 'pay_period_end', 'pay_date', 'status')
    list_filter = ('payroll_type', 'status', 'pay_date', 'pay_period_start')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__username')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'payroll_type', 'amount')
        }),
        ('Hours & Rates', {
            'fields': ('hours_worked', 'hourly_rate')
        }),
        ('Pay Period', {
            'fields': ('pay_period_start', 'pay_period_end', 'pay_date', 'status')
        }),
        ('Additional Information', {
            'fields': ('description', 'processed_by', 'created_at')
        }),
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Expense admin"""
    list_display = ('category', 'description', 'amount', 'expense_date', 'vendor', 'approved_by', 'created_by')
    list_filter = ('category', 'expense_date', 'approved_by', 'created_by')
    search_fields = ('description', 'vendor')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Expense Details', {
            'fields': ('category', 'description', 'amount', 'expense_date', 'vendor')
        }),
        ('Documentation', {
            'fields': ('receipt_file',)
        }),
        ('Approval', {
            'fields': ('approved_by', 'created_by', 'created_at')
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin"""
    list_display = ('invoice_number', 'recipient', 'recipient_type', 'total_amount', 'issue_date', 'due_date', 'status')
    list_filter = ('status', 'recipient_type', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'recipient')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'recipient', 'recipient_type')
        }),
        ('Amounts', {
            'fields': ('amount', 'tax_amount', 'total_amount')
        }),
        ('Dates & Status', {
            'fields': ('issue_date', 'due_date', 'status')
        }),
        ('Content', {
            'fields': ('description', 'items')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at')
        }),
    )


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    """Financial Report admin"""
    list_display = ('title', 'report_type', 'period_start', 'period_end', 'total_revenue', 'total_expenses', 'net_profit', 'generated_by')
    list_filter = ('report_type', 'period_start', 'period_end', 'generated_by')
    search_fields = ('title',)
    readonly_fields = ('generated_at',)
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'report_type', 'period_start', 'period_end')
        }),
        ('Financial Summary', {
            'fields': ('total_revenue', 'total_expenses', 'net_profit')
        }),
        ('Data & Metadata', {
            'fields': ('report_data', 'generated_by', 'generated_at')
        }),
    )
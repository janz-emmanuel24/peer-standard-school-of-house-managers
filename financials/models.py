from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from students.models import Student, Enrollment
from courses.models import Course, Instructor
from employers.models import Employer


class TuitionFee(models.Model):
    """Tuition fees for courses"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tuition_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - ${self.amount} (from {self.effective_date})"

    class Meta:
        verbose_name = "Tuition Fee"
        verbose_name_plural = "Tuition Fees"


class Payment(models.Model):
    """Student payments"""
    PAYMENT_TYPE_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('registration', 'Registration Fee'),
        ('late_fee', 'Late Fee'),
        ('other', 'Other'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('check', 'Check'),
        ('installment', 'Installment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField()
    reference_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    receipt_file = models.FileField(upload_to='receipts/', blank=True, null=True)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_payments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - ${self.amount} ({self.get_payment_type_display()})"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class PlacementFee(models.Model):
    """Placement fees from employers"""
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='placement_fees')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placement_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fee_type = models.CharField(max_length=50)  # e.g., 'placement', 'rehire', 'renewal'
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Payment.STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=Payment.PAYMENT_METHOD_CHOICES, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employer.company_name} - ${self.amount} ({self.fee_type})"

    class Meta:
        verbose_name = "Placement Fee"
        verbose_name_plural = "Placement Fees"


class Payroll(models.Model):
    """Payroll for instructors and staff"""
    PAYROLL_TYPE_CHOICES = [
        ('salary', 'Monthly Salary'),
        ('hourly', 'Hourly Wage'),
        ('commission', 'Commission'),
        ('bonus', 'Bonus'),
        ('overtime', 'Overtime'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payroll_records')
    payroll_type = models.CharField(max_length=20, choices=PAYROLL_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    pay_date = models.DateField()
    status = models.CharField(max_length=20, choices=Payment.STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_payrolls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.get_full_name()} - ${self.amount} ({self.get_payroll_type_display()})"

    class Meta:
        verbose_name = "Payroll"
        verbose_name_plural = "Payroll Records"


class Expense(models.Model):
    """Business expenses"""
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('marketing', 'Marketing'),
        ('training', 'Training'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    expense_date = models.DateField()
    vendor = models.CharField(max_length=200, blank=True)
    receipt_file = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_expenses')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} - ${self.amount} ({self.expense_date})"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


class Invoice(models.Model):
    """Generated invoices"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=100, unique=True)
    recipient = models.CharField(max_length=200)  # Can be student or employer
    recipient_type = models.CharField(max_length=20)  # 'student' or 'employer'
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.TextField()
    items = models.JSONField()  # Store invoice line items
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.recipient} (${self.total_amount})"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"


class FinancialReport(models.Model):
    """Financial reports and summaries"""
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('custom', 'Custom Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    period_start = models.DateField()
    period_end = models.DateField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)
    report_data = models.JSONField()  # Store detailed financial data
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.period_start} to {self.period_end})"

    class Meta:
        verbose_name = "Financial Report"
        verbose_name_plural = "Financial Reports"
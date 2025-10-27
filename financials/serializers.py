from rest_framework import serializers
from .models import TuitionFee, Payment, PlacementFee, Payroll, Expense, Invoice, FinancialReport


class TuitionFeeSerializer(serializers.ModelSerializer):
    """Tuition fee serializer"""
    course_title = serializers.SerializerMethodField()
    
    class Meta:
        model = TuitionFee
        fields = [
            'id', 'course', 'course_title', 'amount', 'effective_date', 
            'expiry_date', 'is_active', 'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_course_title(self, obj):
        return obj.course.title


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'student', 'student_name', 'enrollment', 'course_title', 
            'payment_type', 'amount', 'payment_method', 'status', 'payment_date', 
            'reference_number', 'description', 'receipt_file', 'processed_by', 
            'processed_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_course_title(self, obj):
        return obj.enrollment.course.title if obj.enrollment else None
    
    def get_processed_by_name(self, obj):
        return obj.processed_by.get_full_name()


class PlacementFeeSerializer(serializers.ModelSerializer):
    """Placement fee serializer"""
    employer_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = PlacementFee
        fields = [
            'id', 'employer', 'employer_name', 'student', 'student_name', 
            'amount', 'fee_type', 'due_date', 'paid_date', 'status', 
            'payment_method', 'reference_number', 'invoice_number', 'notes', 
            'is_overdue', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_employer_name(self, obj):
        return obj.employer.company_name
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    
    def get_is_overdue(self, obj):
        if obj.status == 'pending' and obj.due_date:
            from django.utils import timezone
            return timezone.now().date() > obj.due_date
        return False


class PayrollSerializer(serializers.ModelSerializer):
    """Payroll serializer"""
    employee_name = serializers.SerializerMethodField()
    processed_by_name = serializers.SerializerMethodField()
    total_hours_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'employee_name', 'payroll_type', 'amount', 
            'hours_worked', 'hourly_rate', 'total_hours_display', 'pay_period_start', 
            'pay_period_end', 'pay_date', 'status', 'description', 'processed_by', 
            'processed_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_employee_name(self, obj):
        return obj.employee.get_full_name()
    
    def get_processed_by_name(self, obj):
        return obj.processed_by.get_full_name()
    
    def get_total_hours_display(self, obj):
        if obj.hours_worked:
            return f"{obj.hours_worked} hours"
        return None


class ExpenseSerializer(serializers.ModelSerializer):
    """Expense serializer"""
    approved_by_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = [
            'id', 'category', 'category_display', 'description', 'amount', 
            'expense_date', 'vendor', 'receipt_file', 'approved_by', 
            'approved_by_name', 'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name()
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name()
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class InvoiceSerializer(serializers.ModelSerializer):
    """Invoice serializer"""
    created_by_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'recipient', 'recipient_type', 'amount', 
            'tax_amount', 'total_amount', 'issue_date', 'due_date', 'status', 
            'status_display', 'description', 'items', 'is_overdue', 'created_by', 
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name()
    
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_is_overdue(self, obj):
        if obj.status in ['sent', 'pending'] and obj.due_date:
            from django.utils import timezone
            return timezone.now().date() > obj.due_date
        return False


class FinancialReportSerializer(serializers.ModelSerializer):
    """Financial report serializer"""
    generated_by_name = serializers.SerializerMethodField()
    report_type_display = serializers.SerializerMethodField()
    profit_margin = serializers.SerializerMethodField()
    
    class Meta:
        model = FinancialReport
        fields = [
            'id', 'report_type', 'report_type_display', 'title', 'period_start', 
            'period_end', 'total_revenue', 'total_expenses', 'net_profit', 
            'profit_margin', 'report_data', 'generated_by', 'generated_by_name', 
            'generated_at'
        ]
        read_only_fields = ['id', 'generated_at']
    
    def get_generated_by_name(self, obj):
        return obj.generated_by.get_full_name()
    
    def get_report_type_display(self, obj):
        return obj.get_report_type_display()
    
    def get_profit_margin(self, obj):
        if obj.total_revenue > 0:
            return round((obj.net_profit / obj.total_revenue) * 100, 2)
        return 0

from django.db import models

# Create your models here.

class Expense(models.Model):

    EXPENSE_TYPES = (
        ('STOCK', 'Stock Purchase'),
        ('TRANSPORT', 'Transport'),
        ('FUEL', 'Fuel'),
        ('SALARY', 'Salary'),
        ('ELECTRICITY', 'Electricity'),
        ('RENT', 'Rent'),
        ('UTILITY', 'Utility'),
        ('OTHER', 'Other'),
    )
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('MOMO', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )

    expense_type = models.CharField(
        max_length=20,
        choices=EXPENSE_TYPES
    )
    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_METHODS,
    default='CASH'
    )
    transaction_reference = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    recorded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"
    

class DailyReport(models.Model):

    report_date = models.DateField(unique=True)

    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_deposits = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    generated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Report - {self.report_date}"

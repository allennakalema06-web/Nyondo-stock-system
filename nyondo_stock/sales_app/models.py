from django.db import models
from customers_app.models import Customer
from inventory_app.models import Product
# Create your models here.

class Sale(models.Model):

    PAYMENT_STATUS = (
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
        ('CREDIT', 'Credit'),
    )

    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('MOMO', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )
    SALE_SOURCES = (
        ('DIRECT', 'Direct Sale'),
        ('DEPOSIT', 'Deposit Completion'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    attendant = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    sale_source = models.CharField(
        max_length=20,
        choices=SALE_SOURCES,
        default='DIRECT'
    )
    deposit_reference = models.ForeignKey(
        'PendingCreditSale',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_sales'

    )

    subtotal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    transport_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
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
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    
    pending_credit_sale = models.OneToOneField(
    'PendingCreditSale',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )
    completed_sale = models.BooleanField(default=False)
    requires_delivery = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    



class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"

class Payment(models.Model):

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    payment_date = models.DateTimeField(auto_now_add=True)

    received_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

class Receipt(models.Model):

    sale = models.OneToOneField(
        Sale,
        on_delete=models.CASCADE
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_number
    

class PendingCreditSale(models.Model):

    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    balance_remaining = models.DecimalField(max_digits=12, decimal_places=2)

    transport_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )

    approved_for_sale = models.BooleanField(default=False)
    
    is_scheme_order = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True, related_name='approved_credit_sales'
    )

    def __str__(self):
        return f"Pending Credit Sale #{self.id}"

class PendingCreditSaleItem(models.Model):

    pending_sale = models.ForeignKey(
        PendingCreditSale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"        
from django.db import models
from  decimal import Decimal
from django.utils.timezone import now
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    UNIT_CHOICES = [
        ('Bags', 'Bags'),
        ('Pieces', 'Pieces'),
        ('Kgs', 'Kgs'),
        ('Rolls', 'Rolls'),
        ('Tonnes', 'Tonnes'),
        ('Length', 'Length'),
        ('Sheets', 'Sheets'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)

    product_name = models.CharField(max_length=100)

    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)

    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    normal_percentage = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=25
)

    retail_percentage = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=20
    )

    wholesale_percentage = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=10
   )
    normal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    quantity = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=10)
    eligible_for_scheme = models.BooleanField(
    default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_sku(self):
        if not self.sku:
            category_code = (
                self.category.category_name[:3]
                .upper()
            )
            product_code = (
                self.product_name[:4]
                .upper()
            )
            
            import random
            random_number = random.randint(100, 999)
            self.sku = (
                f"{category_code}-{product_code}-{random_number}"
            )

    def calculate_prices(self):
        self.normal_price = (
            self.unit_cost +
            (
                self.unit_cost *
                self.normal_percentage /
                Decimal('100')
            )
        )
        
        self.retail_price = (
            self.unit_cost +
            (
                self.unit_cost *
                self.retail_percentage /
                Decimal('100')
            )
        )
        
        self.wholesale_price = (
            self.unit_cost +
            (
                self.unit_cost *
                self.wholesale_percentage /
                Decimal('100')
            )
        )

    @property
    def pricing_map(self):
        return {
        'NORMAL': self.normal_price,
        'RETAIL': self.retail_price,
        'WHOLESALE': self.wholesale_price,
        }    
    
    def save(self, *args, **kwargs):
        self.generate_sku()
        self.calculate_prices()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name 

    @property
    def available_stock(self):
        return self.quantity   
    
class Supplier(models.Model):

    COMPANY_TYPES = (
        ('SOLE', 'Sole Proprietorship'),
        ('PARTNERSHIP', 'Partnership'),
        ('LLC', 'Limited Liability Company'),
        ('CORPORATION', 'Corporation'),
    )

    supplier_name = models.CharField(max_length=150)

    contact_person = models.CharField(max_length=100)

    job_title = models.CharField(
        max_length=100,
        blank=True
    )

    phone_number = models.CharField(max_length=20)

    alternative_phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(blank=True)

    company_type = models.CharField(
        max_length=30,
        choices=COMPANY_TYPES,
        blank=True
    )

    business_registration_number = models.CharField(
        max_length=100,
        blank=True
    )

    tin_number = models.CharField(
        max_length=100,
        blank=True
    )

    website = models.URLField(blank=True)

    address = models.TextField(blank=True)

    city = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default='Uganda'
    )
    
    balance_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    is_credit_supplier = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.supplier_name
    
class SupplierPayment(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('MOMO', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_METHODS,
    default='BANK'
    )
    transaction_reference = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    payment_date = models.DateTimeField(auto_now_add=True)

    recorded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)    
    
class StockEntry(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('MOMO', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )
    added_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )
    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    stock_date = models.DateField(default=now)

    supplied_on_credit = models.BooleanField(default=False)

    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        blank=True,
        null=True
    )
    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    notes = models.TextField(
        blank=True,
        null=True
    )

    date_added = models.DateTimeField(
        auto_now_add=True
    )

    

    def __str__(self):
        return f"Stock Entry #{self.id}"

class StockEntryItem(models.Model):

    stock_entry = models.ForeignKey(
        StockEntry,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"    
    

class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity_changed = models.IntegerField()

    reason = models.TextField()

    adjusted_at = models.DateTimeField(auto_now_add=True)

    adjusted_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.product.product_name} adjustment"    
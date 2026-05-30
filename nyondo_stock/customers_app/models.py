from django.db import models
from django.utils.timezone import now
# Create your models here.

class Customer(models.Model):

    CUSTOMER_TYPES = (
        ('NORMAL', 'Normal Buyer'),
        ('RETAIL', 'Retailer'),
        ('WHOLESALE', 'Wholesaler'),
    )

    customer_name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=20)

    nin = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True
    )

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPES,
        default='NORMAL'
    )

    address = models.TextField(blank=True)

    balance_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    employer_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
 
    next_of_kin = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    next_of_kin_contact = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_scheme_customer = models.BooleanField(
        default=False
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

class DepositPayment(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('MOMO', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2
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
    remaining_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.amount_paid}"
    
class DeliveryLocation(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    location_name = models.CharField(max_length=200)

    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    transport_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.location_name}"    
    

class TransportDelivery(models.Model):

    DELIVERY_STATUS = (
        ('PENDING', 'Pending'),
        ('ONROUTE', 'On Route'),
        ('DELIVERED', 'Delivered'),
    )

    sale = models.ForeignKey('sales_app.Sale', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    truck_number = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)

    delivery_location = models.ForeignKey(
        DeliveryLocation,
        on_delete=models.SET_NULL,
        null=True
    )

    transport_fee = models.DecimalField(max_digits=12, decimal_places=2)

    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS,
        default='PENDING'
    )
    delivery_address = models.CharField(max_length=255, blank=True, null=True)

    dispatch_date = models.DateTimeField(auto_now_add=True)

    recorded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(default=now)
    

    def __str__(self):
        return f"{self.customer.customer_name} - {self.delivery_status}"   
from django.contrib import admin
from .models import Customer, DepositPayment, DeliveryLocation, TransportDelivery 

# Register your models here.
admin.site.register(Customer)
admin.site.register(DepositPayment)
admin.site.register(DeliveryLocation)
admin.site.register(TransportDelivery)
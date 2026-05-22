from django.contrib import admin
from .models import Sale, SaleItem, Payment, PendingCreditSale, PendingCreditSaleItem, Receipt
# Register your models here.

admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Payment)
admin.site.register(PendingCreditSale)
admin.site.register(PendingCreditSaleItem)
admin.site.register(Receipt)
from django.contrib import admin
from .models import Category, Product, Supplier, SupplierPayment, StockEntry, StockEntryItem, StockAdjustment  

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(SupplierPayment)
admin.site.register(StockEntry)
admin.site.register(StockEntryItem)
admin.site.register(StockAdjustment)
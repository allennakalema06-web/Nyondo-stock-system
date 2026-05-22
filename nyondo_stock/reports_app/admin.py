from django.contrib import admin
from .models import Expense, DailyReport
# Register your models here.

admin.site.register(Expense)
admin.site.register(DailyReport)
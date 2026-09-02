from django.contrib import admin  # pyright: ignore[reportMissingModuleSource]
from .models import UserProfile
# Register your models here.
admin.site.register(UserProfile)

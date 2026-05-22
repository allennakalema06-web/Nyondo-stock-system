from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Stock Manager'),
        ('ATTENDANT', 'Sales Attendant'),
    )

    username = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.username

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username        
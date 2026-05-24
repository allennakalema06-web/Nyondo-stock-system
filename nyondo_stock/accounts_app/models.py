from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username        
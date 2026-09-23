from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('BUYER', 'Buyser / Investor'),
        ('SELLER', 'Property Owner / Seller'),
        ('AGENT', 'Real Estate Agent'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='BUYER')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
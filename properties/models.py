from django.db import models
from django.conf import settings

class Property(models.Model):
    PROPERTY_TYPES = [
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('VILLA', 'Villa'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='HOUSE')
    
    location = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, blank=True, null=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    asking_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    area_sqft = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ${self.price}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_gallery/')
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"
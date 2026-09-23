from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from properties.models import Property

User = get_user_model()

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.sender.username} on {self.property.title}"
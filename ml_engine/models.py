from django.db import models

# Create your models here.
from properties.models import Property
from django.conf import settings

class ValuationLog(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    rooms = models.FloatField()
    lstat = models.FloatField()
    ptratio = models.FloatField()
    crim = models.FloatField()

    predicted_value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
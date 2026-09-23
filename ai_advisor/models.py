from django.db import models

# Create your models here.
from properties.models import Property

class InvestmentReport(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='investment_reports')
    risk_score = models.CharField(max_length=50)
    ai_market_summery = models.TextField()
    negotiation_tips = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
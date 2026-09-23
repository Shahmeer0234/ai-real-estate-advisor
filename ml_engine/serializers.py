from rest_framework import serializers
from .models import ValuationLog

class PredictPriceSerializer(serializers.ModelSerializer):
    rooms = serializers.FloatField(help_text='Average Room Count')
    lstat = serializers.FloatField(help_text='Lower Status Percentage')
    ptratio = serializers.FloatField(help_text='Pupil-Teacher Ratio')
    crim = serializers.FloatField(help_text='Crime Rate')
    property_id = serializers.IntegerField(required=False, allow_null=True)

class ValuationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuationLog
        fields = '__all__'
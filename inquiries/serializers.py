from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    property_title = serializers.ReadOnlyField(source='property.title')

    class Meta:
        model = Inquiry
        fields = ['id', 'property', 'property_title', 'sender', 'message', 'contact_phone', 'created_at']
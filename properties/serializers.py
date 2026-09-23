from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'uploaded_at']

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    images = PropertyImageSerializer(many=True, read_only=True)
   
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'id', 
            'owner', 
            'title', 
            'desciption', 
            'property_type', 
            'city', 
            'asking_price', 
            'image',
            'images',
            'uploaded_images',
            'created_at'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        property_obj = Property.objects.create(**validated_data)
        
        for img in uploaded_images:
            PropertyImage.objects.create(property=property_obj, image=img)
            
        return property_obj
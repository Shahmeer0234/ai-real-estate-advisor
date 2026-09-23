from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from authentication.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'city']
    search_fields = ['title', 'desciption', 'city']
    ordering_fields = ['asking_price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

def home_ui_view(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'properties/home.html', {'properties': properties})

def property_detail_ui_view(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property_obj})

@login_required(login_url='login-ui')
def add_property_ui_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        area_sqft = request.POST.get('area_sqft')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        Property.objects.create(
            owner=request.user,
            title=title,
            description=description,
            price=price,
            area_sqft=area_sqft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            location=location,
            image=image
        )
        return redirect('home')

    return render(request, 'properties/add_property.html')

@login_required(login_url='login-ui')
def my_properties_ui_view(request):
    user_properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'properties/my_properties.html', {'properties': user_properties})


@login_required(login_url='login-ui')
def edit_property_ui_view(request, pk):
    property_obj = get_object_or_404(Property, id=pk, owner=request.user)

    if request.method == 'POST':
        property_obj.title = request.POST.get('title')
        property_obj.location = request.POST.get('location')
        property_obj.price = request.POST.get('price')
        property_obj.area_sqft = request.POST.get('area_sqft')
        property_obj.bedrooms = request.POST.get('bedrooms')
        property_obj.bathrooms = request.POST.get('bathrooms')
        property_obj.description = request.POST.get('description')

        if request.FILES.get('image'):
            property_obj.image = request.FILES.get('image')

        property_obj.save()
        messages.success(request, "Property successfully updated!")
        return redirect('my-properties-ui')

    return render(request, 'properties/edit_property.html', {'property': property_obj})


@login_required(login_url='login-ui')
def delete_property_ui_view(request, pk):
    property_obj = get_object_or_404(Property, id=pk, owner=request.user)
    
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Property successfully deleted!")
        return redirect('my-properties-ui')

    return render(request, 'properties/delete_confirm.html', {'property': property_obj})


def property_list_ui_view(request):
    properties = Property.objects.all().order_by('-created_at')

    # Query parameters GET request se lein
    location_query = request.GET.get('location', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    bedrooms = request.GET.get('bedrooms', '')

    # Filters Apply karein
    if location_query:
        properties = properties.filter(
            Q(location__icontains=location_query) | 
            Q(title__icontains=location_query) |
            Q(city__icontains=location_query)
        )
    
    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    context = {
        'properties': properties,
        'location_query': location_query,
        'min_price': min_price,
        'max_price': max_price,
        'bedrooms': bedrooms,
    }
    return render(request, 'properties/property_list.html', context)
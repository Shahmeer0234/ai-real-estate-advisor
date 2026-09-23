from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework import generics, permissions
from .models import Inquiry
from .serializers import InquirySerializer
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from properties.models import Property


class InquiryListCreateView(generics.ListCreateAPIView):
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Inquiry.objects.filter(models.Q(sender=user) | models.Q(property__owner=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@login_required(login_url='login-ui')
def send_inquiry_ui_view(request, property_id):
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, id=property_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        Inquiry.objects.create(
            property=property_obj,
            sender=request.user,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        messages.success(request, 'Your inquiry has been sent successfully!')
        return redirect('property-detail-ui', pk=property_id)

    return redirect('home')

@login_required(login_url='login-ui')
def my_inquiries_ui_view(request):
    received_inquiries = Inquiry.objects.filter(property__owner=request.user).order_by('-created_at')
    
    sent_inquiries = Inquiry.objects.filter(sender=request.user).order_by('-created_at')

    return render(request, 'inquiries/my_inquiries.html', {
        'received_inquiries': received_inquiries,
        'sent_inquiries': sent_inquiries
    })
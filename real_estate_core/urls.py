"""
URL configuration for real_estate_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties.views import home_ui_view, add_property_ui_view, property_list_ui_view
from authentication.views import login_ui_view, register_ui_view, logout_ui_view
from ml_engine.views import predict_ui_view
from inquiries.views import send_inquiry_ui_view
from ai_advisor.views import ai_report_ui_view

from properties.views import (
    my_properties_ui_view, 
    edit_property_ui_view, 
    delete_property_ui_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('property/<int:property_id>/ai-report/', ai_report_ui_view, name='ai-report-ui'),
    
    path('api/auth/', include('authentication.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/ml/', include('ml_engine.urls')),
    path('api/ai/', include('ai_advisor.urls')),
    path('api/inquiries/', include('inquiries.urls')),

    path('login/', login_ui_view, name='login-ui'),
    path('register/', register_ui_view, name='register-ui'),
    path('logout/', logout_ui_view, name='logout-ui'),

    path('', property_list_ui_view, name='home'),
    path('predict/', predict_ui_view, name='predict-ui'),
    path('add-property/', add_property_ui_view, name='add-property-ui'),

    path('inquiry/send/<int:property_id>/', send_inquiry_ui_view, name='send-inquiry-ui'),

    path('my-properties/', my_properties_ui_view, name='my-properties-ui'),
    path('my-properties/edit/<int:pk>/', edit_property_ui_view, name='edit-property-ui'),
    path('my-properties/delete/<int:pk>/', delete_property_ui_view, name='delete-property-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
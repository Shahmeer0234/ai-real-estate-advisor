from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet
from properties.views import home_ui_view, add_property_ui_view, property_detail_ui_view
from ml_engine.views import predict_ui_view
from . import views

router = DefaultRouter()
router.register(r'listings', PropertyViewSet, basename='property')

urlpatterns = [
    path('api/', include(router.urls)),

    path('', views.property_list_ui_view, name='home'),

    path('', home_ui_view, name='home'),
    path('property/<int:pk>/', property_detail_ui_view, name='property-detail-ui'),
    path('predict/', predict_ui_view, name='predict-ui'),
    path('add-property/', add_property_ui_view, name='add-property-ui'),
]
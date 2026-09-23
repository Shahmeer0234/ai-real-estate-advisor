from django.urls import path
from .views import predict_ui_view, PricePredictionView

urlpatterns = [
    path('predict-price/', predict_ui_view, name='predict-price'),
    path('predict/', PricePredictionView.as_view(), name='api-predict'),
]
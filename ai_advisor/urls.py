from django.urls import path
from .views import GenerateAIReportView

urlpatterns = [
    path('generate-report/<int:property_id>/', GenerateAIReportView.as_view(), name='generate-ai-report'),
]
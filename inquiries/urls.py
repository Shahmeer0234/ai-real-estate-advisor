from django.urls import path
from .views import InquiryListCreateView, my_inquiries_ui_view

urlpatterns = [
    path('', InquiryListCreateView.as_view(), name='inquiry-list-create'),
    path('my-inquiries/', my_inquiries_ui_view, name='my-inquiries-ui'),
]
# contact/urls.py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='index'),
    path('service-request/', views.ServiceRequestView.as_view(), name='service_request'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
]
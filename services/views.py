# services/views.py
from django.views.generic import ListView, DetailView
from core.views import BaseView
from .models import Service

class ServiceListView(BaseView, ListView):
    """قائمة الخدمات"""
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)

class ServiceDetailView(BaseView, DetailView):
    """تفاصيل الخدمة"""
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'

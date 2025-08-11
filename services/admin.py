# services/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """إدارة الخدمات"""
    list_display = ('title_ar', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title_ar', 'title_en', 'title_tr', 'description_ar')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'title_ar')
    
    fieldsets = (
        (_('العناوين'), {
            'fields': ('title_ar', 'title_en', 'title_tr')
        }),
        (_('الأوصاف'), {
            'fields': ('description_ar', 'description_en', 'description_tr')
        }),
        (_('الصورة والأيقونة'), {
            'fields': ('image', 'icon')
        }),
        (_('الإعدادات'), {
            'fields': ('is_active', 'order')
        }),
    )

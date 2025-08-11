# core/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """إدارة إعدادات الموقع"""
    fieldsets = (
        (_('معلومات عامة'), {
            'fields': ('site_name_ar', 'site_name_en', 'site_name_tr', 'logo', 'favicon')
        }),
        (_('نبذة عن المؤسسة'), {
            'fields': ('about_ar', 'about_en', 'about_tr')
        }),
        (_('الرؤية'), {
            'fields': ('vision_ar', 'vision_en', 'vision_tr')
        }),
        (_('الرسالة'), {
            'fields': ('mission_ar', 'mission_en', 'mission_tr')
        }),
        (_('معلومات التواصل'), {
            'fields': ('phone', 'email', 'address_ar', 'address_en', 'address_tr')
        }),
        (_('وسائل التواصل الاجتماعي'), {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'whatsapp')
        }),
        (_('خريطة جوجل'), {
            'fields': ('google_maps_embed',)
        }),
    )
    
    def has_add_permission(self, request):
        """السماح بإضافة إعداد واحد فقط"""
        return not SiteSettings.objects.exists()
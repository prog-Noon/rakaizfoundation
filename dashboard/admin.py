# dashboard/admin.py
from django.contrib import admin
from .models import SiteSettings, UserActivity, DashboardWidget

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('site_name_ar', 'site_name_en', 'tagline_ar', 'tagline_en')
        }),
        ('الوصف', {
            'fields': ('about_ar', 'about_en')
        }),
        ('الصور', {
            'fields': ('logo', 'favicon')
        }),
        ('التواصل', {
            'fields': ('contact_email', 'contact_phone', 'address_ar', 'address_en')
        }),
        ('وسائل التواصل الاجتماعي', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url', 'whatsapp_number')
        }),
        ('SEO', {
            'fields': ('meta_description_ar', 'meta_description_en', 'meta_keywords', 'google_analytics_id')
        }),
        ('إعدادات البريد', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_use_tls')
        }),
    )
    
    def has_add_permission(self, request):
        # السماح بإضافة سجل واحد فقط
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # منع الحذف
        return False

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'action', 'ip_address')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'widget_type', 'position', 'is_active')
    list_filter = ('widget_type', 'is_active')
    ordering = ('position',)

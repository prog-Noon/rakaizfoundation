# team/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """إدارة أعضاء الفريق"""
    list_display = ('name_ar', 'position_ar', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_ar', 'name_en', 'name_tr', 'position_ar', 'email')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'name_ar')
    
    fieldsets = (

        (_('الأسماء'), {
            'fields': ('name_ar', 'name_en', 'name_tr')
        }),
        (_('المناصب'), {
            'fields': ('position_ar', 'position_en', 'position_tr')
        }),
        (_('النبذة التعريفية'), {
            'fields': ('bio_ar', 'bio_en', 'bio_tr')
        }),
        (_('الصورة'), {
            'fields': ('photo',)
        }),
        (_('معلومات التواصل'), {
            'fields': ('email', 'phone')
        }),
        (_('وسائل التواصل الاجتماعي'), {
            'fields': ('facebook', 'linkedin'),
            'classes': ('collapse',)
        }),
        (_('الإعدادات'), {
            'fields': ('is_active', 'order')
        }),
    )
    
    def get_queryset(self, request):
        """ترتيب أعضاء الفريق حسب الترتيب والحالة"""
        return super().get_queryset(request).order_by('order', 'name_ar')
    
    def save_model(self, request, obj, form, change):
        """إجراءات إضافية عند الحفظ"""
        if not change:  # عند الإضافة
            # تعيين ترتيب تلقائي إذا لم يتم تحديده
            if not obj.order:
                last_order = TeamMember.objects.aggregate(
                    max_order=Max('order')
                )['max_order'] or 0
                obj.order = last_order + 1
        
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/team_admin.css',)
        }
        js = ('admin/js/team_admin.js',)
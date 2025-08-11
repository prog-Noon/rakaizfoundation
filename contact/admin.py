# contact/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Count
from .models import ContactMessage, ServiceRequest

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """إدارة رسائل التواصل"""
    list_display = ('name', 'email', 'contact_type', 'subject', 'read_status', 'reply_status', 'created_at','is_read', 'is_replied')
    list_filter = ('contact_type', 'is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read', 'is_replied')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_unread']
    
    fieldsets = (
        (_('معلومات المرسل'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('تفاصيل الرسالة'), {
            'fields': ('contact_type', 'subject', 'message')
        }),
        (_('حالة الرسالة'), {
            'fields': ('is_read', 'is_replied')
        }),
        (_('التواريخ'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def read_status(self, obj):
        """عرض حالة القراءة بألوان"""
        if obj.is_read:
            return format_html(
                '<span class="badge bg-success">تم القراءة</span>'
            )
        return format_html(
            '<span class="badge bg-warning">لم يُقرأ</span>'
        )
    read_status.short_description = _('حالة القراءة')
    
    def reply_status(self, obj):
        """عرض حالة الرد بألوان"""
        if obj.is_replied:
            return format_html(
                '<span class="badge bg-primary">تم الرد</span>'
            )
        return format_html(
            '<span class="badge bg-secondary">لم يتم الرد</span>'
        )
    reply_status.short_description = _('حالة الرد')
    
    def get_queryset(self, request):
        """ترتيب الرسائل حسب الحالة والتاريخ"""
        return super().get_queryset(request).order_by('is_read', '-created_at')
    
    # Actions للتعامل مع الرسائل
    def mark_as_read(self, request, queryset):
        """وضع علامة مقروء"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'تم وضع علامة مقروء على {updated} رسالة')
    mark_as_read.short_description = _('وضع علامة مقروء')
    
    def mark_as_replied(self, request, queryset):
        """وضع علامة تم الرد"""
        updated = queryset.update(is_replied=True, is_read=True)
        self.message_user(request, f'تم وضع علامة تم الرد على {updated} رسالة')
    mark_as_replied.short_description = _('وضع علامة تم الرد')
    
    def mark_as_unread(self, request, queryset):
        """وضع علامة غير مقروء"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'تم وضع علامة غير مقروء على {updated} رسالة')
    mark_as_unread.short_description = _('وضع علامة غير مقروء')

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """إدارة طلبات الخدمات"""
    list_display = ('name', 'service', 'priority_display', 'status_display', 'preferred_date', 'created_at','priority', 'status')
    list_filter = ('service', 'priority', 'status', 'created_at', 'preferred_date')
    search_fields = ('name', 'email', 'phone', 'description')
    list_editable = ('priority', 'status')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_cancelled']
    
    fieldsets = (
        (_('معلومات مقدم الطلب'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('تفاصيل الطلب'), {
            'fields': ('service', 'description', 'preferred_date')
        }),
        (_('إدارة الطلب'), {
            'fields': ('priority', 'status')
        }),
        (_('التواريخ'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_display(self, obj):
        """عرض الأولوية بألوان"""
        colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'urgent': 'dark'
        }
        color = colors.get(obj.priority, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_display.short_description = _('الأولوية')
    
    def status_display(self, obj):
        """عرض الحالة بألوان"""
        colors = {
            'pending': 'warning',
            'processing': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = _('الحالة')
    
    def get_queryset(self, request):
        """ترتيب الطلبات حسب الحالة والأولوية"""
        return super().get_queryset(request).order_by('status', '-priority', '-created_at')
    
    # Actions لإدارة الطلبات
    def mark_as_processing(self, request, queryset):
        """تحديد الحالة إلى قيد المعالجة"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'تم تحديث {updated} طلب إلى حالة قيد المعالجة')
    mark_as_processing.short_description = _('تحديد كـ قيد المعالجة')
    
    def mark_as_completed(self, request, queryset):
        """تحديد الحالة إلى مكتمل"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'تم تحديث {updated} طلب إلى حالة مكتمل')
    mark_as_completed.short_description = _('تحديد كـ مكتمل')
    
    def mark_as_cancelled(self, request, queryset):
        """تحديد الحالة إلى ملغي"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'تم تحديث {updated} طلب إلى حالة ملغي')
    mark_as_cancelled.short_description = _('تحديد كـ ملغي')
    
    def changelist_view(self, request, extra_context=None):
        """إضافة إحصائيات إلى صفحة القائمة"""
        extra_context = extra_context or {}
        
        # إحصائيات الطلبات
        extra_context['stats'] = {
            'total': ServiceRequest.objects.count(),
            'pending': ServiceRequest.objects.filter(status='pending').count(),
            'processing': ServiceRequest.objects.filter(status='processing').count(),
            'completed': ServiceRequest.objects.filter(status='completed').count(),
            'cancelled': ServiceRequest.objects.filter(status='cancelled').count(),
        }
        
        return super().changelist_view(request, extra_context=extra_context)

# تخصيص واجهة الإدارة
admin.site.site_header = _('لوحة تحكم مؤسسة ركائز')
admin.site.site_title = _('إدارة مؤسسة ركائز')
admin.site.index_title = _('مرحباً بك في لوحة التحكم')
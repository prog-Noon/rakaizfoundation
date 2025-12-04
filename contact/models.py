# contact/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel

class ContactMessage(BaseModel):
    """رسائل التواصل"""
    CONTACT_TYPES = [
        ('general', _('عام')),
        ('service', _('استفسار عن خدمة')),
        ('appointment', _('طلب موعد')),
        ('complaint', _('شكوى')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('الاسم'))
    email = models.EmailField(verbose_name=_('البريد الإلكتروني'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('رقم الهاتف'))
    
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='general', verbose_name=_('نوع الرسالة'))
    subject = models.CharField(max_length=200, verbose_name=_('الموضوع'))
    message = models.TextField(verbose_name=_('الرسالة'))
    
    is_read = models.BooleanField(default=False, verbose_name=_('تم القراءة'))
    is_replied = models.BooleanField(default=False, verbose_name=_('تم الرد'))
    
    class Meta:
        verbose_name = _('رسالة تواصل')
        verbose_name_plural = _('رسائل التواصل')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class ServiceRequest(BaseModel):  # ← لا تضف MultilingualMixin هنا
    """طلبات الخدمات"""
    PRIORITY_CHOICES = [
        ('low', _('منخفض')),
        ('medium', _('متوسط')),
        ('high', _('عالي')),
        ('urgent', _('عاجل')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('في الانتظار')),
        ('processing', _('قيد المعالجة')),
        ('completed', _('مكتمل')),
        ('cancelled', _('ملغي')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('الاسم'))
    email = models.EmailField(verbose_name=_('البريد الإلكتروني'))
    phone = models.CharField(max_length=20, verbose_name=_('رقم الهاتف'))
    
    service = models.ForeignKey(
        'services.Service', 
        on_delete=models.CASCADE, 
        verbose_name=_('الخدمة'),
        related_name='contact_requests'
    )
    description = models.TextField(verbose_name=_('وصف الطلب'))
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name=_('الأولوية'))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name=_('الحالة'))
    
    preferred_date = models.DateField(blank=True, null=True, verbose_name=_('التاريخ المفضل'))
    
    admin_notes = models.TextField(blank=True, verbose_name=_('ملاحظات الإدارة'))
    response_date = models.DateTimeField(blank=True, null=True, verbose_name=_('تاريخ الرد'))
    
    class Meta:
        verbose_name = _('طلب خدمة')
        verbose_name_plural = _('طلبات الخدمات')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.service.title}"  # ✅ هذا صحيح - service.title سيستخدم Mixin تلقائياً
    
    def mark_as_processing(self):
        self.status = 'processing'
        self.save(update_fields=['status'])
    
    def mark_as_completed(self):
        self.status = 'completed'
        from django.utils import timezone
        self.response_date = timezone.now()
        self.save(update_fields=['status', 'response_date'])
    
    @property
    def is_urgent(self):
        return self.priority == 'urgent'
    
    @property
    def status_color(self):
        colors = {
            'pending': 'warning',
            'processing': 'info', 
            'completed': 'success',
            'cancelled': 'danger'
        }
        return colors.get(self.status, 'secondary')
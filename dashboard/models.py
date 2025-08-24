# dashboard/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class DashboardWidget(models.Model):
    """عنصر في لوحة التحكم"""
    title_ar = models.CharField(_('العنوان بالعربية'), max_length=100)
    title_en = models.CharField(_('العنوان بالإنجليزية'), max_length=100, blank=True)
    widget_type = models.CharField(_('نوع العنصر'), max_length=50, choices=[
        ('stats', 'إحصائيات'),
        ('chart', 'رسم بياني'),
        ('table', 'جدول'),
        ('quick_actions', 'إجراءات سريعة'),
    ])
    position = models.PositiveIntegerField(_('الموضع'), default=0)
    is_active = models.BooleanField(_('نشط'), default=True)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)

    class Meta:
        verbose_name = _('عنصر لوحة التحكم')
        verbose_name_plural = _('عناصر لوحة التحكم')
        ordering = ['position']

    def __str__(self):
        return self.title_ar

class UserActivity(models.Model):
    """نشاط المستخدمين"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('المستخدم'))
    action = models.CharField(_('الإجراء'), max_length=100)
    model_name = models.CharField(_('نوع النموذج'), max_length=50, blank=True)
    object_id = models.PositiveIntegerField(_('معرف الكائن'), blank=True, null=True)
    timestamp = models.DateTimeField(_('الوقت'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('عنوان IP'), blank=True, null=True)

    class Meta:
        verbose_name = _('نشاط المستخدم')
        verbose_name_plural = _('أنشطة المستخدمين')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action}"

class SiteSettings(models.Model):
    """إعدادات الموقع"""
    site_name_ar = models.CharField(_('اسم الموقع بالعربية'), max_length=100)
    site_name_en = models.CharField(_('اسم الموقع بالإنجليزية'), max_length=100, blank=True)
    tagline_ar = models.CharField(_('الشعار بالعربية'), max_length=200, blank=True)
    tagline_en = models.CharField(_('الشعار بالإنجليزية'), max_length=200, blank=True)
    about_ar = models.TextField(_('عن الموقع بالعربية'), blank=True)
    about_en = models.TextField(_('عن الموقع بالإنجليزية'), blank=True)
    logo = models.ImageField(_('الشعار'), upload_to='settings/', blank=True)
    favicon = models.ImageField(_('أيقونة المتصفح'), upload_to='settings/', blank=True)
    contact_email = models.EmailField(_('بريد التواصل'))
    contact_phone = models.CharField(_('هاتف التواصل'), max_length=20, blank=True)
    address_ar = models.TextField(_('العنوان بالعربية'), blank=True)
    address_en = models.TextField(_('العنوان بالإنجليزية'), blank=True)
    
    # إعدادات وسائل التواصل
    facebook_url = models.URLField(_('رابط فيسبوك'), blank=True)
    twitter_url = models.URLField(_('رابط تويتر'), blank=True)
    instagram_url = models.URLField(_('رابط إنستغرام'), blank=True)
    linkedin_url = models.URLField(_('رابط لينكد إن'), blank=True)
    youtube_url = models.URLField(_('رابط يوتيوب'), blank=True)
    whatsapp_number = models.CharField(_('رقم واتساب'), max_length=20, blank=True)
    
    # إعدادات SEO
    meta_description_ar = models.TextField(_('وصف الموقع للبحث (عربي)'), blank=True, max_length=160)
    meta_description_en = models.TextField(_('وصف الموقع للبحث (إنجليزي)'), blank=True, max_length=160)
    meta_keywords = models.TextField(_('الكلمات المفتاحية'), blank=True)
    google_analytics_id = models.CharField(_('معرف جوجل التحليلات'), max_length=50, blank=True)
    
    # إعدادات البريد
    smtp_host = models.CharField(_('خادم البريد'), max_length=100, blank=True)
    smtp_port = models.IntegerField(_('منفذ البريد'), default=587)
    smtp_username = models.CharField(_('اسم مستخدم البريد'), max_length=100, blank=True)
    smtp_password = models.CharField(_('كلمة مرور البريد'), max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(_('استخدام TLS'), default=True)
    
    updated_at = models.DateTimeField(_('آخر تحديث'), auto_now=True)

    class Meta:
        verbose_name = _('إعدادات الموقع')
        verbose_name_plural = _('إعدادات الموقع')

    def __str__(self):
        return self.site_name_ar

    def save(self, *args, **kwargs):
        # التأكد من وجود سجل واحد فقط
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("يمكن أن يكون هناك إعداد موقع واحد فقط")
        return super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """الحصول على إعدادات الموقع"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name_ar': 'مؤسسة ركائز',
                'site_name_en': 'Rakaez Foundation',
                'contact_email': 'info@rakaez.com'
            }
        )
        return obj


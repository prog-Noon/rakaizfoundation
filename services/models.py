# services/models.py
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from ckeditor.fields import RichTextField

class ServiceCategory(BaseModel):
    """فئات الخدمات"""
    name_ar = models.CharField(max_length=100, verbose_name=_('الاسم - عربي'))
    name_en = models.CharField(max_length=100, verbose_name=_('الاسم - إنجليزي'))
    name_tr = models.CharField(max_length=100, verbose_name=_('الاسم - تركي'))
    
    description_ar = models.TextField(blank=True, verbose_name=_('الوصف - عربي'))
    description_en = models.TextField(blank=True, verbose_name=_('الوصف - إنجليزي'))
    description_tr = models.TextField(blank=True, verbose_name=_('الوصف - تركي'))
    
    icon = models.CharField(max_length=50, blank=True, help_text=_('اسم الأيقونة من Font Awesome'), verbose_name=_('الأيقونة'))
    color = models.CharField(max_length=7, default='#6b73ff', help_text=_('كود اللون HEX'), verbose_name=_('اللون'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('ترتيب العرض'))
    
    class Meta:
        verbose_name = _('فئة الخدمات')
        verbose_name_plural = _('فئات الخدمات')
        ordering = ['order', 'name_ar']
    
    def __str__(self):
        return self.name_ar


class Service(BaseModel):
    """نموذج الخدمات"""
    title_ar = models.CharField(max_length=200, verbose_name=_('العنوان - عربي'))
    title_en = models.CharField(max_length=200, verbose_name=_('العنوان - إنجليزي'))
    title_tr = models.CharField(max_length=200, verbose_name=_('العنوان - تركي'))
    
    description_ar = RichTextField(verbose_name=_('الوصف - عربي'))
    description_en = RichTextField(verbose_name=_('الوصف - إنجليزي'))
    description_tr = RichTextField(verbose_name=_('الوصف - تركي'))
    
    # ملخص قصير للخدمة
    excerpt_ar = models.TextField(max_length=300, blank=True, verbose_name=_('ملخص - عربي'))
    excerpt_en = models.TextField(max_length=300, blank=True, verbose_name=_('ملخص - إنجليزي'))
    excerpt_tr = models.TextField(max_length=300, blank=True, verbose_name=_('ملخص - تركي'))
    
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name=_('الصورة'))
    icon = models.CharField(max_length=50, blank=True, help_text=_('اسم الأيقونة من Font Awesome'), verbose_name=_('الأيقونة'))
    
    # فئة الخدمة
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, 
                               verbose_name=_('الفئة'), related_name='services')
    
    # معلومات إضافية
    duration = models.CharField(max_length=100, blank=True, verbose_name=_('مدة الخدمة'))
    target_audience = models.CharField(max_length=200, blank=True, verbose_name=_('الفئة المستهدفة'))
    prerequisites = models.TextField(blank=True, verbose_name=_('المتطلبات المسبقة'))
    
    # ميزات الخدمة (JSON field للمرونة)
    features = models.JSONField(default=list, blank=True, verbose_name=_('ميزات الخدمة'))
    
    # معلومات التكلفة
    is_free = models.BooleanField(default=True, verbose_name=_('مجانية'))
    cost = models.CharField(max_length=100, blank=True, verbose_name=_('التكلفة'))
    
    # خيارات العرض
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    is_featured = models.BooleanField(default=False, verbose_name=_('مميز'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('ترتيب العرض'))
    
    # إحصائيات
    views = models.PositiveIntegerField(default=0, verbose_name=_('عدد المشاهدات'))
    requests_count = models.PositiveIntegerField(default=0, verbose_name=_('عدد الطلبات'))
    
    class Meta:
        verbose_name = _('خدمة')
        verbose_name_plural = _('الخدمات')
        ordering = ['order', 'title_ar']
    
    def __str__(self):
        return self.title_ar
    
    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'pk': self.pk})
    
    @property
    def get_excerpt(self):
        """إرجاع الملخص أو جزء من الوصف"""
        if self.excerpt_ar:
            return self.excerpt_ar
        # إزالة HTML tags والحصول على أول 150 حرف
        import re
        clean_description = re.sub(r'<[^>]+>', '', self.description_ar)
        return clean_description[:150] + '...' if len(clean_description) > 150 else clean_description
    
    @property
    def get_features_list(self):
        """إرجاع قائمة بالميزات"""
        if isinstance(self.features, list):
            return self.features
        return []
    
    def increment_views(self):
        """زيادة عدد المشاهدات"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def increment_requests(self):
        """زيادة عدد الطلبات"""
        self.requests_count += 1
        self.save(update_fields=['requests_count'])
    
    @property
    def total_requests(self):
        """إجمالي طلبات هذه الخدمة"""
        return self.contact_requests.count()
    
    @property
    def pending_requests(self):
        """الطلبات المعلقة لهذه الخدمة"""
        return self.contact_requests.filter(status='pending').count()
    
    @property
    def completed_requests(self):
        """الطلبات المكتملة لهذه الخدمة"""
        return self.contact_requests.filter(status='completed').count()
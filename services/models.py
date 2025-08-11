# services/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from ckeditor.fields import RichTextField

class Service(BaseModel):
    """نموذج الخدمات"""
    title_ar = models.CharField(max_length=200, verbose_name=_('العنوان - عربي'))
    title_en = models.CharField(max_length=200, verbose_name=_('العنوان - إنجليزي'))
    title_tr = models.CharField(max_length=200, verbose_name=_('العنوان - تركي'))
    
    description_ar = RichTextField(verbose_name=_('الوصف - عربي'))
    description_en = RichTextField(verbose_name=_('الوصف - إنجليزي'))
    description_tr = RichTextField(verbose_name=_('الوصف - تركي'))
    
    image = models.ImageField(upload_to='services/', verbose_name=_('الصورة'))
    icon = models.CharField(max_length=50, blank=True, help_text=_('اسم الأيقونة من Font Awesome'), verbose_name=_('الأيقونة'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('ترتيب العرض'))
    
    class Meta:
        verbose_name = _('خدمة')
        verbose_name_plural = _('الخدمات')
        ordering = ['order', 'title_ar']
    
    def __str__(self):
        return self.title_ar
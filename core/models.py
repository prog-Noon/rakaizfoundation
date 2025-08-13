# core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class BaseModel(models.Model):
    """نموذج أساسي لجميع النماذج الأخرى"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))
    
    class Meta:
        abstract = True

class SiteSettings(models.Model):
    """إعدادات الموقع العامة"""
    site_name_ar = models.CharField(max_length=100, default="مؤسسة ركائز", verbose_name=_('اسم الموقع - عربي'))
    site_name_en = models.CharField(max_length=100, default="Rakayez Foundation", verbose_name=_('اسم الموقع - إنجليزي'))
    site_name_tr = models.CharField(max_length=100, default="Rakayez Vakfı", verbose_name=_('اسم الموقع - تركي'))
    
    logo = models.ImageField(upload_to='settings/', verbose_name=_('الشعار'),blank=True,
    null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, verbose_name=_('أيقونة المتصفح'))
    
    about_ar = RichTextField(verbose_name=_('نبذة عن المؤسسة - عربي'))
    about_en = RichTextField(verbose_name=_('نبذة عن المؤسسة - إنجليزي'))
    about_tr = RichTextField(verbose_name=_('نبذة عن المؤسسة - تركي'))
    
    vision_ar = RichTextField(verbose_name=_('الرؤية - عربي'))
    vision_en = RichTextField(verbose_name=_('الرؤية - إنجليزي'))
    vision_tr = RichTextField(verbose_name=_('الرؤية - تركي'))
    
    mission_ar = RichTextField(verbose_name=_('الرسالة - عربي'))
    mission_en = RichTextField(verbose_name=_('الرسالة - إنجليزي'))
    mission_tr = RichTextField(verbose_name=_('الرسالة - تركي'))
    
    phone = models.CharField(max_length=20, verbose_name=_('رقم الهاتف'))
    email = models.EmailField(verbose_name=_('البريد الإلكتروني'))
    address_ar = models.TextField(verbose_name=_('العنوان - عربي'))
    address_en = models.TextField(verbose_name=_('العنوان - إنجليزي'))
    address_tr = models.TextField(verbose_name=_('العنوان - تركي'))
    
    facebook = models.URLField(blank=True, verbose_name=_('فيسبوك'))
    instagram = models.URLField(blank=True, verbose_name=_('إنستغرام'))
    twitter = models.URLField(blank=True, verbose_name=_('تويتر'))
    linkedin = models.URLField(blank=True, verbose_name=_('لينكدإن'))
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name=_('واتساب'))
    
    google_maps_embed = models.TextField(blank=True, verbose_name=_('خريطة جوجل'))
    
    class Meta:
        verbose_name = _('إعدادات الموقع')
        verbose_name_plural = _('إعدادات الموقع')
    
    def __str__(self):
        return self.site_name_ar
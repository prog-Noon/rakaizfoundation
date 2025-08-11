# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

class NewsCategory(BaseModel):
    """تصنيفات الأخبار"""
    name_ar = models.CharField(max_length=100, verbose_name=_('الاسم - عربي'))
    name_en = models.CharField(max_length=100, verbose_name=_('الاسم - إنجليزي'))
    name_tr = models.CharField(max_length=100, verbose_name=_('الاسم - تركي'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    
    class Meta:
        verbose_name = _('تصنيف الأخبار')
        verbose_name_plural = _('تصنيفات الأخبار')
    
    def __str__(self):
        return self.name_ar

class News(BaseModel):
    """نموذج الأخبار والأنشطة"""
    title_ar = models.CharField(max_length=200, verbose_name=_('العنوان - عربي'))
    title_en = models.CharField(max_length=200, verbose_name=_('العنوان - إنجليزي'))
    title_tr = models.CharField(max_length=200, verbose_name=_('العنوان - تركي'))
    
    content_ar = RichTextUploadingField(verbose_name=_('المحتوى - عربي'))
    content_en = RichTextUploadingField(verbose_name=_('المحتوى - إنجليزي'))
    content_tr = RichTextUploadingField(verbose_name=_('المحتوى - تركي'))
    
    excerpt_ar = models.TextField(max_length=300, verbose_name=_('ملخص - عربي'))
    excerpt_en = models.TextField(max_length=300, verbose_name=_('ملخص - إنجليزي'))
    excerpt_tr = models.TextField(max_length=300, verbose_name=_('ملخص - تركي'))
    
    featured_image = models.ImageField(upload_to='news/', verbose_name=_('الصورة البارزة'))
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name=_('التصنيف'))
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('الكاتب'))
    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ النشر'))
    
    is_published = models.BooleanField(default=True, verbose_name=_('منشور'))
    is_featured = models.BooleanField(default=False, verbose_name=_('مميز'))
    
    views = models.PositiveIntegerField(default=0, verbose_name=_('عدد المشاهدات'))
    
    class Meta:
        verbose_name = _('خبر')
        verbose_name_plural = _('الأخبار')
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title_ar
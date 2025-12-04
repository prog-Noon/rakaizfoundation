# team/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from core.mixins import MultilingualMixin

class TeamMember(MultilingualMixin, BaseModel):
    """نموذج أعضاء الفريق"""
    name_ar = models.CharField(max_length=100, verbose_name=_('الاسم - عربي'))
    name_en = models.CharField(max_length=100, verbose_name=_('الاسم - إنجليزي'))
    name_tr = models.CharField(max_length=100, verbose_name=_('الاسم - تركي'))
    
    position_ar = models.CharField(max_length=100, verbose_name=_('المنصب - عربي'))
    position_en = models.CharField(max_length=100, verbose_name=_('المنصب - إنجليزي'))
    position_tr = models.CharField(max_length=100, verbose_name=_('المنصب - تركي'))
    
    bio_ar = models.TextField(blank=True, verbose_name=_('نبذة - عربي'))
    bio_en = models.TextField(blank=True, verbose_name=_('نبذة - إنجليزي'))
    bio_tr = models.TextField(blank=True, verbose_name=_('نبذة - تركي'))
    
    photo = models.ImageField(upload_to='team/', verbose_name=_('الصورة'))
    
    email = models.EmailField(blank=True, verbose_name=_('البريد الإلكتروني'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('رقم الهاتف'))
    
    facebook = models.URLField(blank=True, verbose_name=_('فيسبوك'))
    linkedin = models.URLField(blank=True, verbose_name=_('لينكدإن'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('ترتيب العرض'))
    
    class Meta:
        verbose_name = _('عضو الفريق')
        verbose_name_plural = _('أعضاء الفريق')
        ordering = ['order', 'name_ar']
    
    def __str__(self):
        return self.name

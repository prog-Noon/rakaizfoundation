# core/mixins.py
"""
Mixin لإضافة دعم متعدد اللغات للنماذج
"""
from django.utils.translation import get_language

class MultilingualMixin:
    """
    Mixin لإضافة properties ديناميكية تُرجع القيمة المناسبة حسب اللغة الحالية
    
    الاستخدام:
    1. أضف هذا الـ Mixin إلى Model الذي يحتوي على حقول متعددة اللغات
    2. استخدم get_field() في templates/views بدلاً من الحقول المباشرة
    
    مثال في Model:
        class News(MultilingualMixin, BaseModel):
            title_ar = models.CharField(...)
            title_en = models.CharField(...)
            title_tr = models.CharField(...)
    
    مثال في Template:
        {{ news.get_field('title') }}  # بدلاً من news.title_ar
    """
    
    def get_field(self, field_name, fallback_lang='ar'):
        """
        الحصول على قيمة الحقل حسب اللغة الحالية
        
        Args:
            field_name: اسم الحقل بدون اللغة (مثل 'title' بدلاً من 'title_ar')
            fallback_lang: اللغة الافتراضية إذا لم يكن للحقل قيمة باللغة الحالية
        
        Returns:
            قيمة الحقل باللغة المناسبة
        """
        current_lang = get_language()
        
        # محاولة الحصول على القيمة باللغة الحالية
        field_with_lang = f"{field_name}_{current_lang}"
        value = getattr(self, field_with_lang, None)
        
        # إذا كانت القيمة فارغة، جرّب اللغة الافتراضية
        if not value:
            field_with_fallback = f"{field_name}_{fallback_lang}"
            value = getattr(self, field_with_fallback, '')
        
        return value
    
    @property
    def title(self):
        """العنوان باللغة الحالية"""
        return self.get_field('title')
    
    @property
    def description(self):
        """الوصف باللغة الحالية"""
        return self.get_field('description')
    
    @property
    def content(self):
        """المحتوى باللغة الحالية"""
        return self.get_field('content')
    
    @property
    def excerpt(self):
        """الملخص باللغة الحالية"""
        return self.get_field('excerpt')
    
    @property
    def name(self):
        """الاسم باللغة الحالية"""
        return self.get_field('name')
    
    @property
    def position(self):
        """المنصب باللغة الحالية"""
        return self.get_field('position')
    
    @property
    def bio(self):
        """النبذة باللغة الحالية"""
        return self.get_field('bio')
    
    @property
    def about(self):
        """نبذة باللغة الحالية"""
        return self.get_field('about')
    
    @property
    def vision(self):
        """الرؤية باللغة الحالية"""
        return self.get_field('vision')
    
    @property
    def mission(self):
        """الرسالة باللغة الحالية"""
        return self.get_field('mission')
    
    @property
    def address(self):
        """العنوان باللغة الحالية"""
        return self.get_field('address')
    
    @property
    def site_name(self):
        """اسم الموقع باللغة الحالية"""
        return self.get_field('site_name')
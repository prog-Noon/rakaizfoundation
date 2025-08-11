
# news/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import News, NewsCategory

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """إدارة تصنيفات الأخبار"""
    list_display = ('name_ar', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_ar', 'name_en', 'name_tr')
    list_editable = ('is_active',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """إدارة الأخبار"""
    list_display = ('title_ar', 'category', 'author', 'is_published', 'is_featured', 'views', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category', 'published_at', 'created_at')
    search_fields = ('title_ar', 'title_en', 'title_tr', 'excerpt_ar')
    list_editable = ('is_published', 'is_featured')
    readonly_fields = ('views', 'published_at')
    date_hierarchy = 'published_at'
    
    fieldsets = (
        (_('العناوين'), {
            'fields': ('title_ar', 'title_en', 'title_tr')
        }),
        (_('الملخصات'), {
            'fields': ('excerpt_ar', 'excerpt_en', 'excerpt_tr')
        }),
        (_('المحتوى'), {
            'fields': ('content_ar', 'content_en', 'content_tr')
        }),
        (_('الصورة والتصنيف'), {
            'fields': ('featured_image', 'category')
        }),
        (_('الإعدادات'), {
            'fields': ('is_published', 'is_featured', 'author')
        }),
        (_('الإحصائيات'), {
            'fields': ('views', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """تعيين المؤلف تلقائياً"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

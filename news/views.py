# news/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.views import BaseContextMixin
from .models import News, NewsCategory

class NewsListView(BaseContextMixin, ListView):
    """قائمة الأخبار"""
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True).select_related(
            'category', 'author'
        ).order_by('-published_at')
        
        # البحث
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title_ar__icontains=search) |
                Q(title_en__icontains=search) |
                Q(title_tr__icontains=search) |
                Q(excerpt_ar__icontains=search) |
                Q(excerpt_en__icontains=search) |
                Q(excerpt_tr__icontains=search) |
                Q(content_ar__icontains=search) |
                Q(content_en__icontains=search) |
                Q(content_tr__icontains=search)
            )
        
        # التصفية حسب الفئة
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass
        
        # التصفية حسب المميز
        featured = self.request.GET.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إضافة الفئات للتصفية
        context['categories'] = NewsCategory.objects.filter(is_active=True).order_by('name_ar')
        
        # إضافة الأخبار المميزة للسايدبار (إذا لم تكن مفلترة)
        if not self.request.GET.get('featured'):
            context['featured_news'] = News.objects.filter(
                is_published=True, 
                is_featured=True
            ).order_by('-published_at')[:3]
        
        # إضافة معاملات البحث
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['is_featured_filter'] = self.request.GET.get('featured') == 'true'
        
        return context


class NewsDetailView(BaseContextMixin, DetailView):
    """تفاصيل الخبر"""
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            'category', 'author'
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # زيادة عدد المشاهدات
        News.objects.filter(pk=obj.pk).update(views=obj.views + 1)
        # تحديث الكائن المحلي
        obj.views += 1
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # الأخبار ذات الصلة (نفس الفئة)
        context['related_news'] = News.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by('-published_at')[:3]
        
        # الخبر السابق والتالي
        try:
            context['previous_news'] = News.objects.filter(
                is_published=True,
                published_at__lt=self.object.published_at
            ).order_by('-published_at').first()
        except:
            context['previous_news'] = None
            
        try:
            context['next_news'] = News.objects.filter(
                is_published=True,
                published_at__gt=self.object.published_at
            ).order_by('published_at').first()
        except:
            context['next_news'] = None
        
        # الأخبار الحديثة للسايدبار
        context['recent_news'] = News.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk).order_by('-published_at')[:5]
        
        return context


class NewsCategoryView(BaseContextMixin, ListView):
    """أخبار حسب التصنيف"""
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(
            NewsCategory, 
            pk=self.kwargs['pk'], 
            is_active=True
        )
        return News.objects.filter(
            is_published=True, 
            category=self.category
        ).select_related('category', 'author').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = NewsCategory.objects.filter(
            is_active=True
        ).exclude(pk=self.category.pk).order_by('name_ar')
        
        # الأخبار المميزة من نفس الفئة
        context['featured_news'] = News.objects.filter(
            is_published=True,
            is_featured=True,
            category=self.category
        ).order_by('-published_at')[:3]
        
        return context


# View إضافي للأخبار المميزة فقط
class FeaturedNewsView(BaseContextMixin, ListView):
    """الأخبار المميزة فقط"""
    model = News
    template_name = 'news/featured.html'
    context_object_name = 'news_list'
    paginate_by = 6
    
    def get_queryset(self):
        return News.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('category', 'author').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'الأخبار المميزة'
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        return context


# View للبحث في الأخبار
class NewsSearchView(BaseContextMixin, ListView):
    """البحث في الأخبار"""
    model = News
    template_name = 'news/search.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return News.objects.none()
        
        return News.objects.filter(
            Q(title_ar__icontains=query) |
            Q(title_en__icontains=query) |
            Q(title_tr__icontains=query) |
            Q(excerpt_ar__icontains=query) |
            Q(excerpt_en__icontains=query) |
            Q(excerpt_tr__icontains=query) |
            Q(content_ar__icontains=query) |
            Q(content_en__icontains=query) |
            Q(content_tr__icontains=query),
            is_published=True
        ).select_related('category', 'author').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        return context
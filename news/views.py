# news/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from core.views import BaseView
from .models import News, NewsCategory

class NewsListView(BaseView, ListView):
    """قائمة الأخبار"""
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title_ar__icontains=search) |
                Q(title_en__icontains=search) |
                Q(title_tr__icontains=search) |
                Q(excerpt_ar__icontains=search) |
                Q(excerpt_en__icontains=search) |
                Q(excerpt_tr__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['featured_news'] = News.objects.filter(is_published=True, is_featured=True)[:3]
        return context

class NewsDetailView(BaseView, DetailView):
    """تفاصيل الخبر"""
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    
    def get_object(self):
        obj = super().get_object()
        # زيادة عدد المشاهدات
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context

class NewsCategoryView(BaseView, ListView):
    """أخبار حسب التصنيف"""
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = NewsCategory.objects.get(pk=self.kwargs['pk'])
        return News.objects.filter(is_published=True, category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        return context


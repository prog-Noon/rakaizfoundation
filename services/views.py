# services/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from core.views import BaseContextMixin
from .models import Service, ServiceCategory

class ServiceListView(BaseContextMixin, ListView):
    """قائمة الخدمات"""
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related('category').order_by('order', 'title_ar')
        
        # البحث
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title_ar__icontains=search_query) |
                Q(title_en__icontains=search_query) |
                Q(title_tr__icontains=search_query) |
                Q(description_ar__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                Q(description_tr__icontains=search_query)
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
        
        # التصفية حسب المجاني
        free_only = self.request.GET.get('free')
        if free_only == 'true':
            queryset = queryset.filter(is_free=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إضافة الفئات للتصفية
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order', 'name_ar')
        
        # إضافة الخدمات المميزة
        context['featured_services'] = Service.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('order')[:6]
        
        # إضافة إحصائيات
        context['total_services'] = Service.objects.filter(is_active=True).count()
        context['free_services_count'] = Service.objects.filter(is_active=True, is_free=True).count()
        
        # إضافة معاملات البحث
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['is_featured_filter'] = self.request.GET.get('featured') == 'true'
        context['is_free_filter'] = self.request.GET.get('free') == 'true'
        
        return context


class ServiceDetailView(BaseContextMixin, DetailView):
    """تفاصيل الخدمة"""
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # زيادة عدد المشاهدات
        Service.objects.filter(pk=obj.pk).update(views=obj.views + 1)
        obj.views += 1
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إضافة الخدمات الأخرى (باستثناء الخدمة الحالية)
        context['other_services'] = Service.objects.filter(
            is_active=True
        ).exclude(pk=self.object.pk).order_by('order')[:5]
        
        # إضافة خدمات من نفس الفئة
        if self.object.category:
            context['related_services'] = Service.objects.filter(
                is_active=True,
                category=self.object.category
            ).exclude(pk=self.object.pk).order_by('order')[:3]
        else:
            # خدمات عشوائية إذا لم تكن هناك فئة
            context['related_services'] = Service.objects.filter(
                is_active=True
            ).exclude(pk=self.object.pk).order_by('?')[:3]
        
        # إضافة الخدمات المميزة للسايدبار
        context['featured_services'] = Service.objects.filter(
            is_active=True,
            is_featured=True
        ).exclude(pk=self.object.pk).order_by('order')[:4]
        
        return context


class ServiceCategoryView(BaseContextMixin, ListView):
    """خدمات حسب الفئة"""
    model = Service
    template_name = 'services/category.html'
    context_object_name = 'services'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(
            ServiceCategory, 
            pk=self.kwargs['pk'], 
            is_active=True
        )
        return Service.objects.filter(
            is_active=True, 
            category=self.category
        ).order_by('order', 'title_ar')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = ServiceCategory.objects.filter(
            is_active=True
        ).exclude(pk=self.category.pk).order_by('order', 'name_ar')
        
        # الخدمات المميزة من نفس الفئة
        context['featured_services'] = Service.objects.filter(
            is_active=True,
            is_featured=True,
            category=self.category
        ).order_by('order')[:3]
        
        return context


class FeaturedServicesView(BaseContextMixin, ListView):
    """الخدمات المميزة فقط"""
    model = Service
    template_name = 'services/featured.html'
    context_object_name = 'services'
    paginate_by = 8
    
    def get_queryset(self):
        return Service.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category').order_by('order', 'title_ar')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'الخدمات المميزة'
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        return context
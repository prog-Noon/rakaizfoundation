# dashboard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from core.models import SiteSettings
from news.models import News, NewsCategory
from services.models import Service
from team.models import TeamMember
from contact.models import ContactMessage, ServiceRequest

class SuperuserRequiredMixin(UserPassesTestMixin):
    """التأكد من أن المستخدم هو مدير عام"""
    def test_func(self):
        return self.request.user.is_superuser

class DashboardBaseView(LoginRequiredMixin, SuperuserRequiredMixin):
    """عرض أساسي للوحة التحكم"""
    pass

class DashboardHomeView(DashboardBaseView, TemplateView):
    """الصفحة الرئيسية للوحة التحكم"""
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إحصائيات عامة
        context['stats'] = {
            'total_news': News.objects.count(),
            'total_services': Service.objects.count(),
            'total_team_members': TeamMember.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'pending_requests': ServiceRequest.objects.filter(status='pending').count(),
        }
        
        # الأخبار الأخيرة
        context['recent_news'] = News.objects.order_by('-created_at')[:5]
        
        # الرسائل الجديدة
        context['recent_messages'] = ContactMessage.objects.filter(is_read=False).order_by('-created_at')[:5]
        
        # طلبات الخدمات الجديدة
        context['recent_requests'] = ServiceRequest.objects.filter(status='pending').order_by('-created_at')[:5]
        
        return context

class SettingsView(DashboardBaseView, TemplateView):
    """إدارة إعدادات الموقع"""
    template_name = 'dashboard/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['settings'] = SiteSettings.objects.first()
        except SiteSettings.DoesNotExist:
            context['settings'] = SiteSettings.objects.create()
        return context

# إدارة الأخبار
class NewsManagementView(DashboardBaseView, ListView):
    """قائمة الأخبار"""
    model = News
    template_name = 'dashboard/news/list.html'
    context_object_name = 'news_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = News.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title_ar__icontains=search) | Q(title_en__icontains=search)
            )
        return queryset

class NewsCreateView(DashboardBaseView, CreateView):
    """إضافة خبر جديد"""
    model = News
    template_name = 'dashboard/news/form.html'
    fields = ['title_ar', 'title_en', 'title_tr', 'content_ar', 'content_en', 'content_tr', 
              'excerpt_ar', 'excerpt_en', 'excerpt_tr', 'featured_image', 'category', 
              'is_published', 'is_featured']
    success_url = reverse_lazy('dashboard:news_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _('تم إنشاء الخبر بنجاح'))
        return super().form_valid(form)

class NewsUpdateView(DashboardBaseView, UpdateView):
    """تعديل خبر"""
    model = News
    template_name = 'dashboard/news/form.html'
    fields = ['title_ar', 'title_en', 'title_tr', 'content_ar', 'content_en', 'content_tr', 
              'excerpt_ar', 'excerpt_en', 'excerpt_tr', 'featured_image', 'category', 
              'is_published', 'is_featured']
    success_url = reverse_lazy('dashboard:news_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث الخبر بنجاح'))
        return super().form_valid(form)

class NewsDeleteView(DashboardBaseView, DeleteView):
    """حذف خبر"""
    model = News
    success_url = reverse_lazy('dashboard:news_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف الخبر بنجاح'))
        return super().delete(request, *args, **kwargs)

# إدارة الخدمات
class ServiceManagementView(DashboardBaseView, ListView):
    """قائمة الخدمات"""
    model = Service
    template_name = 'dashboard/services/list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.all().order_by('order')

class ServiceCreateView(DashboardBaseView, CreateView):
    """إضافة خدمة جديدة"""
    model = Service
    template_name = 'dashboard/services/form.html'
    fields = ['title_ar', 'title_en', 'title_tr', 'description_ar', 'description_en', 
              'description_tr', 'image', 'icon', 'is_active', 'order']
    success_url = reverse_lazy('dashboard:service_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم إنشاء الخدمة بنجاح'))
        return super().form_valid(form)

class ServiceUpdateView(DashboardBaseView, UpdateView):
    """تعديل خدمة"""
    model = Service
    template_name = 'dashboard/services/form.html'
    fields = ['title_ar', 'title_en', 'title_tr', 'description_ar', 'description_en', 
              'description_tr', 'image', 'icon', 'is_active', 'order']
    success_url = reverse_lazy('dashboard:service_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث الخدمة بنجاح'))
        return super().form_valid(form)

class ServiceDeleteView(DashboardBaseView, DeleteView):
    """حذف خدمة"""
    model = Service
    success_url = reverse_lazy('dashboard:service_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف الخدمة بنجاح'))
        return super().delete(request, *args, **kwargs)

# إدارة الفريق
class TeamManagementView(DashboardBaseView, ListView):
    """قائمة أعضاء الفريق"""
    model = TeamMember
    template_name = 'dashboard/team/list.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        return TeamMember.objects.all().order_by('order')

class TeamCreateView(DashboardBaseView, CreateView):
    """إضافة عضو فريق جديد"""
    model = TeamMember
    template_name = 'dashboard/team/form.html'
    fields = ['name_ar', 'name_en', 'name_tr', 'position_ar', 'position_en', 'position_tr',
              'bio_ar', 'bio_en', 'bio_tr', 'photo', 'email', 'phone', 'facebook', 'linkedin',
              'is_active', 'order']
    success_url = reverse_lazy('dashboard:team_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم إضافة عضو الفريق بنجاح'))
        return super().form_valid(form)

class TeamUpdateView(DashboardBaseView, UpdateView):
    """تعديل عضو فريق"""
    model = TeamMember
    template_name = 'dashboard/team/form.html'
    fields = ['name_ar', 'name_en', 'name_tr', 'position_ar', 'position_en', 'position_tr',
              'bio_ar', 'bio_en', 'bio_tr', 'photo', 'email', 'phone', 'facebook', 'linkedin',
              'is_active', 'order']
    success_url = reverse_lazy('dashboard:team_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث بيانات عضو الفريق بنجاح'))
        return super().form_valid(form)

class TeamDeleteView(DashboardBaseView, DeleteView):
    """حذف عضو فريق"""
    model = TeamMember
    success_url = reverse_lazy('dashboard:team_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف عضو الفريق بنجاح'))
        return super().delete(request, *args, **kwargs)

# إدارة الرسائل
class MessagesView(DashboardBaseView, ListView):
    """قائمة رسائل التواصل"""
    model = ContactMessage
    template_name = 'dashboard/messages/list.html'
    context_object_name = 'messages'
    paginate_by = 20
    
    def get_queryset(self):
        return ContactMessage.objects.all().order_by('-created_at')

class MessageDetailView(DashboardBaseView, TemplateView):
    """تفاصيل رسالة التواصل"""
    template_name = 'dashboard/messages/detail.html'
    
    def get_object(self):
        obj = get_object_or_404(ContactMessage, pk=self.kwargs['pk'])
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.get_object()
        return context

class ServiceRequestsView(DashboardBaseView, ListView):
    """قائمة طلبات الخدمات"""
    model = ServiceRequest
    template_name = 'dashboard/requests/list.html'
    context_object_name = 'requests'
    paginate_by = 20
    
    def get_queryset(self):
        return ServiceRequest.objects.all().order_by('-created_at')

class ServiceRequestDetailView(DashboardBaseView, TemplateView):
    """تفاصيل طلب الخدمة"""
    template_name = 'dashboard/requests/detail.html'
    
    def get_object(self):
        return get_object_or_404(ServiceRequest, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.get_object()
        return context
    
    def post(self, request, *args, **kwargs):
        """تحديث حالة الطلب"""
        obj = self.get_object()
        new_status = request.POST.get('status')
        if new_status in dict(ServiceRequest.STATUS_CHOICES):
            obj.status = new_status
            obj.save()
            messages.success(request, _('تم تحديث حالة الطلب بنجاح'))
        return redirect('dashboard:service_request_detail', pk=obj.pk)

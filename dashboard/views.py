
# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta, datetime
import json

# استيراد النماذج من التطبيقات الأخرى
from services.models import Service, ServiceRequest
from news.models import Article
from contact.models import ContactMessage
from .models import SiteSettings, UserActivity, DashboardWidget

def is_admin_user(user):
    """التحقق من أن المستخدم مدير"""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin_user)
def dashboard_home(request):
    """الصفحة الرئيسية للوحة التحكم"""
    
    # الإحصائيات العامة
    total_services = Service.objects.count()
    total_articles = Article.objects.count()
    total_messages = ContactMessage.objects.count()
    total_service_requests = ServiceRequest.objects.count()
    total_users = User.objects.count()
    
    # الإحصائيات الأسبوعية
    week_ago = timezone.now() - timedelta(days=7)
    new_messages_week = ContactMessage.objects.filter(created_at__gte=week_ago).count()
    new_requests_week = ServiceRequest.objects.filter(created_at__gte=week_ago).count()
    new_articles_week = Article.objects.filter(created_at__gte=week_ago).count()
    
    # آخر الرسائل
    recent_messages = ContactMessage.objects.select_related().order_by('-created_at')[:5]
    
    # آخر طلبات الخدمات
    recent_requests = ServiceRequest.objects.select_related('service').order_by('-created_at')[:5]
    
    # آخر المقالات
    recent_articles = Article.objects.filter(status='published').order_by('-created_at')[:5]
    
    # النشاط الحديث
    recent_activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:10]
    
    # إحصائيات الرسائل حسب الحالة
    messages_stats = ContactMessage.objects.aggregate(
        total=Count('id'),
        unread=Count('id', filter=Q(is_read=False)),
        read=Count('id', filter=Q(is_read=True)),
    )
    
    # إحصائيات طلبات الخدمات حسب الحالة
    requests_stats = ServiceRequest.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        completed=Count('id', filter=Q(status='completed')),
        cancelled=Count('id', filter=Q(status='cancelled')),
    )
    
    # بيانات الرسم البياني للرسائل (آخر 7 أيام)
    messages_chart_data = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        count = ContactMessage.objects.filter(created_at__date=date).count()
        messages_chart_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    messages_chart_data.reverse()
    
    context = {
        'total_services': total_services,
        'total_articles': total_articles,
        'total_messages': total_messages,
        'total_service_requests': total_service_requests,
        'total_users': total_users,
        'new_messages_week': new_messages_week,
        'new_requests_week': new_requests_week,
        'new_articles_week': new_articles_week,
        'recent_messages': recent_messages,
        'recent_requests': recent_requests,
        'recent_articles': recent_articles,
        'recent_activities': recent_activities,
        'messages_stats': messages_stats,
        'requests_stats': requests_stats,
        'messages_chart_data': json.dumps(messages_chart_data),
        'current_time': timezone.now(),
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
@user_passes_test(is_admin_user)
def services_dashboard(request):
    """لوحة تحكم الخدمات"""
    services = Service.objects.all().order_by('-created_at')
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(
            Q(title_ar__icontains=search_query) |
            Q(title_en__icontains=search_query) |
            Q(description_ar__icontains=search_query)
        )
    
    # التصفية حسب الحالة
    status_filter = request.GET.get('status', '')
    if status_filter:
        services = services.filter(is_active=(status_filter == 'active'))
    
    # الترقيم
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    services_page = paginator.get_page(page_number)
    
    # إحصائيات الخدمات
    services_stats = {
        'total': Service.objects.count(),
        'active': Service.objects.filter(is_active=True).count(),
        'inactive': Service.objects.filter(is_active=False).count(),
        'with_image': Service.objects.exclude(image='').count(),
    }
    
    context = {
        'services': services_page,
        'services_stats': services_stats,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/services.html', context)

@login_required
@user_passes_test(is_admin_user)
def news_dashboard(request):
    """لوحة تحكم الأخبار"""
    articles = Article.objects.all().order_by('-created_at')
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        articles = articles.filter(
            Q(title_ar__icontains=search_query) |
            Q(title_en__icontains=search_query) |
            Q(content_ar__icontains=search_query)
        )
    
    # التصفية حسب الحالة
    status_filter = request.GET.get('status', '')
    if status_filter:
        articles = articles.filter(status=status_filter)
    
    # الترقيم
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    
    # إحصائيات المقالات
    articles_stats = {
        'total': Article.objects.count(),
        'published': Article.objects.filter(status='published').count(),
        'draft': Article.objects.filter(status='draft').count(),
        'archived': Article.objects.filter(status='archived').count(),
        'featured': Article.objects.filter(is_featured=True).count(),
    }
    
    context = {
        'articles': articles_page,
        'articles_stats': articles_stats,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/news.html', context)

@login_required
@user_passes_test(is_admin_user)
def messages_dashboard(request):
    """لوحة تحكم الرسائل"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    
    # التصفية حسب الحالة
    status_filter = request.GET.get('status', '')
    if status_filter == 'unread':
        messages_list = messages_list.filter(is_read=False)
    elif status_filter == 'read':
        messages_list = messages_list.filter(is_read=True)
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        messages_list = messages_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    # الترقيم
    paginator = Paginator(messages_list, 15)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/messages.html', context)

@login_required
@user_passes_test(is_admin_user)
def settings_dashboard(request):
    """إعدادات الموقع"""
    settings_obj = SiteSettings.get_settings()
    
    if request.method == 'POST':
        # تحديث الإعدادات
        settings_obj.site_name_ar = request.POST.get('site_name_ar', '')
        settings_obj.site_name_en = request.POST.get('site_name_en', '')
        settings_obj.tagline_ar = request.POST.get('tagline_ar', '')
        settings_obj.tagline_en = request.POST.get('tagline_en', '')
        settings_obj.about_ar = request.POST.get('about_ar', '')
        settings_obj.about_en = request.POST.get('about_en', '')
        settings_obj.contact_email = request.POST.get('contact_email', '')
        settings_obj.contact_phone = request.POST.get('contact_phone', '')
        settings_obj.address_ar = request.POST.get('address_ar', '')
        settings_obj.address_en = request.POST.get('address_en', '')
        
        # وسائل التواصل
        settings_obj.facebook_url = request.POST.get('facebook_url', '')
        settings_obj.twitter_url = request.POST.get('twitter_url', '')
        settings_obj.instagram_url = request.POST.get('instagram_url', '')
        settings_obj.linkedin_url = request.POST.get('linkedin_url', '')
        settings_obj.youtube_url = request.POST.get('youtube_url', '')
        settings_obj.whatsapp_number = request.POST.get('whatsapp_number', '')
        
        # إعدادات SEO
        settings_obj.meta_description_ar = request.POST.get('meta_description_ar', '')
        settings_obj.meta_description_en = request.POST.get('meta_description_en', '')
        settings_obj.meta_keywords = request.POST.get('meta_keywords', '')
        settings_obj.google_analytics_id = request.POST.get('google_analytics_id', '')
        
        # رفع الملفات
        if 'logo' in request.FILES:
            settings_obj.logo = request.FILES['logo']
        if 'favicon' in request.FILES:
            settings_obj.favicon = request.FILES['favicon']
        
        settings_obj.save()
        messages.success(request, 'تم حفظ الإعدادات بنجاح!')
        return redirect('dashboard:settings')
    
    context = {
        'settings': settings_obj,
    }
    
    return render(request, 'dashboard/settings.html', context)

@login_required
@user_passes_test(is_admin_user)
def users_dashboard(request):
    """إدارة المستخدمين"""
    users = User.objects.all().order_by('-date_joined')
    
    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # التصفية
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    
    # الترقيم
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    # إحصائيات المستخدمين
    users_stats = {
        'total': User.objects.count(),
        'active': User.objects.filter(is_active=True).count(),
        'staff': User.objects.filter(is_staff=True).count(),
        'superusers': User.objects.filter(is_superuser=True).count(),
    }
    
    context = {
        'users': users_page,
        'users_stats': users_stats,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/users.html', context)

# API Views للرسوم البيانية والإحصائيات
@login_required
@user_passes_test(is_admin_user)
def stats_api(request):
    """API للإحصائيات والرسوم البيانية"""
    chart_type = request.GET.get('type', 'messages')
    
    if chart_type == 'messages':
        # رسم بياني للرسائل لآخر 30 يوم
        data = []
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            count = ContactMessage.objects.filter(created_at__date=date).count()
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        data.reverse()
        
    elif chart_type == 'services':
        # إحصائيات الخدمات
        data = list(Service.objects.values('category').annotate(count=Count('id')))
        
    elif chart_type == 'users':
        # نمو المستخدمين لآخر 12 شهر
        data = []
        for i in range(12):
            date = timezone.now().replace(day=1) - timedelta(days=30*i)
            count = User.objects.filter(date_joined__month=date.month, date_joined__year=date.year).count()
            data.append({
                'month': date.strftime('%Y-%m'),
                'count': count
            })
        data.reverse()
    
    else:
        data = []
    
    return JsonResponse({'data': data})

def log_user_activity(user, action, model_name=None, object_id=None, request=None):
    """تسجيل نشاط المستخدم"""
    ip_address = None
    if request:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    
    UserActivity.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        ip_address=ip_address
    )
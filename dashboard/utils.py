
# dashboard/utils.py
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from services.models import Service, ServiceRequest
from news.models import Article
from contact.models import ContactMessage
from django.contrib.auth.models import User

def get_dashboard_stats():
    """الحصول على إحصائيات Dashboard"""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    stats = {
        # الإحصائيات العامة
        'total_services': Service.objects.count(),
        'total_articles': Article.objects.filter(status='published').count(),
        'total_messages': ContactMessage.objects.count(),
        'total_service_requests': ServiceRequest.objects.count(),
        'total_users': User.objects.count(),
        
        # الإحصائيات الأسبوعية
        'new_messages_week': ContactMessage.objects.filter(created_at__gte=week_ago).count(),
        'new_requests_week': ServiceRequest.objects.filter(created_at__gte=week_ago).count(),
        'new_articles_week': Article.objects.filter(created_at__gte=week_ago, status='published').count(),
        'new_users_week': User.objects.filter(date_joined__gte=week_ago).count(),
        
        # الإحصائيات الشهرية
        'new_messages_month': ContactMessage.objects.filter(created_at__gte=month_ago).count(),
        'new_requests_month': ServiceRequest.objects.filter(created_at__gte=month_ago).count(),
        
        # إحصائيات تفصيلية
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'pending_requests': ServiceRequest.objects.filter(status='pending').count(),
        'active_services': Service.objects.filter(is_active=True).count(),
        'featured_articles': Article.objects.filter(is_featured=True, status='published').count(),
    }
    
    return stats

def get_chart_data(chart_type, days=30):
    """الحصول على بيانات الرسوم البيانية"""
    data = []
    
    for i in range(days):
        date = timezone.now().date() - timedelta(days=i)
        
        if chart_type == 'messages':
            count = ContactMessage.objects.filter(created_at__date=date).count()
        elif chart_type == 'requests':
            count = ServiceRequest.objects.filter(created_at__date=date).count()
        elif chart_type == 'articles':
            count = Article.objects.filter(created_at__date=date, status='published').count()
        else:
            count = 0
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return list(reversed(data))

def get_recent_activities(limit=10):
    """الحصول على آخر الأنشطة"""
    activities = []
    
    # آخر الرسائل
    recent_messages = ContactMessage.objects.order_by('-created_at')[:limit//2]
    for message in recent_messages:
        activities.append({
            'type': 'message',
            'title': f'رسالة جديدة من {message.name}',
            'description': message.subject,
            'timestamp': message.created_at,
            'url': f'/dashboard/messages/?id={message.id}'
        })
    
    # آخر طلبات الخدمات
    recent_requests = ServiceRequest.objects.select_related('service').order_by('-created_at')[:limit//2]
    for request in recent_requests:
        activities.append({
            'type': 'request',
            'title': f'طلب خدمة جديد من {request.name}',
            'description': f'طلب للخدمة: {request.service.title_ar}',
            'timestamp': request.created_at,
            'url': f'/admin/services/servicerequest/{request.id}/change/'
        })
    
    # ترتيب حسب التاريخ
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    return activities[:limit]

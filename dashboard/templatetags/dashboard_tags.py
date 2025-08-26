# dashboard/templatetags/dashboard_tags.py
from django import template
from django.contrib.auth.models import User
from services.models import Service  # Service only from services
from contact.models import ContactMessage, ServiceRequest  # ServiceRequest from contact
from news.models import News  # Changed from Article to News
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.inclusion_tag('dashboard/widgets/stats_widget.html')
def stats_widget():
    """عنصر الإحصائيات"""
    stats = {
        'total_services': Service.objects.count(),
        'total_articles': News.objects.count(),  # Changed from Article to News
        'total_messages': ContactMessage.objects.count(),
        'total_users': User.objects.count(),
    }
    return {'stats': stats}

@register.inclusion_tag('dashboard/widgets/recent_messages.html')
def recent_messages_widget():
    """عنصر آخر الرسائل"""
    messages = ContactMessage.objects.order_by('-created_at')[:5]
    return {'messages': messages}

@register.inclusion_tag('dashboard/widgets/quick_actions.html')
def quick_actions_widget():
    """عنصر الإجراءات السريعة"""
    return {}

@register.filter
def percentage(value, total):
    """حساب النسبة المئوية"""
    if not total:
        return 0
    return round((value / total) * 100, 1)

@register.filter
def time_since_arabic(value):
    """الوقت منذ بالعربية"""
    if not value:
        return ''
    
    now = timezone.now()
    diff = now - value
    
    if diff.days > 0:
        if diff.days == 1:
            return 'منذ يوم واحد'
        elif diff.days < 11:
            return f'منذ {diff.days} أيام'
        else:
            return f'منذ {diff.days} يوماً'
    
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        if hours == 1:
            return 'منذ ساعة واحدة'
        elif hours < 11:
            return f'منذ {hours} ساعات'
        else:
            return f'منذ {hours} ساعة'
    
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        if minutes == 1:
            return 'منذ دقيقة واحدة'
        elif minutes < 11:
            return f'منذ {minutes} دقائق'
        else:
            return f'منذ {minutes} دقيقة'
    
    else:
        return 'الآن'
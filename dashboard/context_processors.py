# dashboard/context_processors.py
from .models import SiteSettings

def site_settings(request):
    """إضافة إعدادات الموقع لجميع الصفحات"""
    try:
        settings = SiteSettings.get_settings()
        return {'site_settings': settings}
    except:
        return {'site_settings': None}

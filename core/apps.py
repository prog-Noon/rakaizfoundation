# core/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _('الإعدادات الأساسية')

# news/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = _('الأخبار والأنشطة')

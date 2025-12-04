"""
Django settings for rakayez_foundation project.
Optimized for production deployment on cPanel.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# يجب وضع SECRET_KEY في ملف .env أو متغيرات البيئة
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-CHANGE-THIS-IN-PRODUCTION-123456789')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# المضيفون المسموح بهم
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'rakaizfoundation.org', 'www.rakaizfoundation.org']
# إعدادات الأمان للإنتاج
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # إعادة توجيه HTTP إلى HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # سنة واحدة
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'ckeditor_uploader',
    
    # Local apps
    'core',
    'news',
    'services',
    'team',
    'contact',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rakayez_foundation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',  # إضافة للوصول للميديا
                'django.template.context_processors.static',  # إضافة للوصول للستاتيك
                'dashboard.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'rakayez_foundation.wsgi.application'

# ==============================================================================
# DATABASE
# ==============================================================================

# للإنتاج: استخدم MySQL من cPanel
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        } if os.environ.get('DB_ENGINE') == 'django.db.backends.mysql' else {},
    }
}

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ar', _('العربية')),
    ('en', _('English')),
    ('tr', _('Türkçe')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ==============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==============================================================================
# MEDIA FILES (User Uploads)
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CRISPY FORMS
# ==============================================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==============================================================================
# CKEDITOR
# ==============================================================================

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'language': 'ar',
        'extraPlugins': ','.join([
            'uploadimage',
            'image2',
        ]),
    },
}

# السماح بأنواع الملفات المرفوعة
CKEDITOR_ALLOW_NONIMAGE_FILES = True
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

# للتطوير
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # للإنتاج - استخدم SMTP من cPanel
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'mail.rakaizfoundation.org')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'info@rakaizfoundation.org')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'info@rakaizfoundation.org')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ==============================================================================
# SITE FRAMEWORK
# ==============================================================================

SITE_ID = 1

# ==============================================================================
# LOGGING (للإنتاج)
# ==============================================================================

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'django_errors.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

# ==============================================================================
# ADMIN SETTINGS
# ==============================================================================

# تخصيص عنوان لوحة الإدارة
ADMIN_SITE_HEADER = "مؤسسة ركائز - لوحة الإدارة"
ADMIN_SITE_TITLE = "إدارة الموقع"
ADMIN_INDEX_TITLE = "مرحباً بك في لوحة إدارة مؤسسة ركائز"
# dashboard/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .views import log_user_activity

class UserActivityMiddleware(MiddlewareMixin):
    """Middleware لتسجيل أنشطة المستخدمين"""
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            # تسجيل النشاط فقط للمدراء
            action = f"زيارة {view_func.__name__}"
            log_user_activity(request.user, action, request=request)
        return None


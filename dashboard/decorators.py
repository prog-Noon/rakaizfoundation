
# dashboard/decorators.py
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied

def admin_required(function):
    """Decorator للتأكد من أن المستخدم مدير"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap

def superuser_required(function):
    """Decorator للتأكد من أن المستخدم superuser"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap
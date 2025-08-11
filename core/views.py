# core/views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.translation import activate
from django.http import JsonResponse
from django.utils import translation
from .models import SiteSettings
from news.models import News
from services.models import Service
from team.models import TeamMember

class BaseView(TemplateView):
    """عرض أساسي لجميع العروض"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['site_settings'] = SiteSettings.objects.first()
        except SiteSettings.DoesNotExist:
            context['site_settings'] = None
        return context

class HomeView(BaseView):
    """الصفحة الرئيسية"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_news'] = News.objects.filter(is_published=True, is_featured=True)[:3]
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['team_members'] = TeamMember.objects.filter(is_active=True)[:4]
        return context

class AboutView(BaseView):
    """صفحة من نحن"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        return context

def set_language(request, language):
    """تغيير اللغة"""
    activate(language)
    request.session['django_language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))

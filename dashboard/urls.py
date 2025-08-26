# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('services/', views.services_dashboard, name='services'),
    path('news/', views.news_dashboard, name='news'),
    path('messages/', views.messages_dashboard, name='messages'),
    path('users/', views.users_dashboard, name='users'),
    path('settings/', views.settings_dashboard, name='settings'),
    path('api/stats/', views.stats_api, name='stats_api'),
    path('services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
]


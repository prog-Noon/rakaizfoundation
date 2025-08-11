# dashboard/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.DashboardHomeView.as_view(), name='home'),
    
    # إدارة الإعدادات
    path('settings/', views.SettingsView.as_view(), name='settings'),
    
    # إدارة الأخبار
    path('news/', views.NewsManagementView.as_view(), name='news_list'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    
    # إدارة الخدمات
    path('services/', views.ServiceManagementView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    # إدارة الفريق
    path('team/', views.TeamManagementView.as_view(), name='team_list'),
    path('team/create/', views.TeamCreateView.as_view(), name='team_create'),
    path('team/<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
    
    # إدارة الرسائل
    path('messages/', views.MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('service-requests/', views.ServiceRequestsView.as_view(), name='service_requests'),
    path('service-requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service_request_detail'),
]

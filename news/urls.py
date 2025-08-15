# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # قائمة الأخبار الرئيسية
    path('', views.NewsListView.as_view(), name='list'),
    
    # الأخبار المميزة
    path('featured/', views.FeaturedNewsView.as_view(), name='featured'),
    
    # البحث في الأخبار
    path('search/', views.NewsSearchView.as_view(), name='search'),
    
    # أخبار حسب الفئة
    path('category/<int:pk>/', views.NewsCategoryView.as_view(), name='category'),
    
    # تفاصيل الخبر
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
]
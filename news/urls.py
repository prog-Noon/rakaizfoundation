# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.NewsCategoryView.as_view(), name='category'),
]

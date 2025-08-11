# team/urls.py
from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='list'),
    path('<int:pk>/', views.TeamMemberDetailView.as_view(), name='detail'),
]

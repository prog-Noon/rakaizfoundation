# team/views.py
from django.views.generic import ListView, DetailView
from core.views import BaseView
from .models import TeamMember

class TeamListView(BaseView, ListView):
    """قائمة أعضاء الفريق"""
    model = TeamMember
    template_name = 'team/list.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)

class TeamMemberDetailView(BaseView, DetailView):
    """تفاصيل عضو الفريق"""
    model = TeamMember
    template_name = 'team/detail.html'
    context_object_name = 'member'

from django.core.management.base import BaseCommand
from dashboard.models import SiteSettings, DashboardWidget

class Command(BaseCommand):
    help = 'إعداد Dashboard الأولي'

    def handle(self, *args, **options):
        # إنشاء إعدادات الموقع الأولية
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name_ar': 'مؤسسة ركائز',
                'site_name_en': 'Rakaez Foundation',
                'tagline_ar': 'لأن المرأة جوهر التغيير',
                'tagline_en': 'Because Women are the Core of Change',
                'contact_email': 'info@rakaez.org',
                'about_ar': 'مؤسسة تنموية توعوية تُعنى بتفعيل دور المرأة السورية عبر برامج ومبادرات نوعية',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('تم إنشاء إعدادات الموقع بنجاح!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('إعدادات الموقع موجودة بالفعل')
            )
        
        # إنشاء عناصر Dashboard الافتراضية
        widgets = [
            {
                'title_ar': 'إحصائيات عامة',
                'title_en': 'General Statistics',
                'widget_type': 'stats',
                'position': 1
            },
            {
                'title_ar': 'الرسائل الحديثة',
                'title_en': 'Recent Messages',
                'widget_type': 'table',
                'position': 2
            },
            {
                'title_ar': 'رسم بياني للنمو',
                'title_en': 'Growth Chart',
                'widget_type': 'chart',
                'position': 3
            },
            {
                'title_ar': 'إجراءات سريعة',
                'title_en': 'Quick Actions',
                'widget_type': 'quick_actions',
                'position': 4
            },
        ]
        
        for widget_data in widgets:
            widget, created = DashboardWidget.objects.get_or_create(
                title_ar=widget_data['title_ar'],
                defaults=widget_data
            )
            if created:
                self.stdout.write(f"تم إنشاء عنصر: {widget_data['title_ar']}")
        
        self.stdout.write(
            self.style.SUCCESS('تم إعداد Dashboard بنجاح!')
        )

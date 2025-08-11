# contact/views.py
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from core.views import BaseView
from .forms import ContactForm, ServiceRequestForm, AppointmentForm
from .models import ContactMessage, ServiceRequest

class ContactView(BaseView, FormView):
    """صفحة التواصل"""
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:index')
    
    def form_valid(self, form):
        # حفظ الرسالة
        message = form.save()
        
        # إرسال إشعار بريد إلكتروني للمدراء (اختياري)
        try:
            send_mail(
                subject=f'رسالة جديدة من الموقع: {message.subject}',
                message=f'''
                رسالة جديدة من: {message.name}
                البريد الإلكتروني: {message.email}
                نوع الرسالة: {message.get_contact_type_display()}
                الموضوع: {message.subject}
                
                نص الرسالة:
                {message.message}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except:
            pass  # في حالة فشل الإرسال، لا نريد إيقاف العملية
        
        messages.success(self.request, _('تم إرسال رسالتك بنجاح. سنتواصل معك قريباً'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى'))
        return super().form_invalid(form)

class ServiceRequestView(BaseView, FormView):
    """طلب خدمة"""
    template_name = 'contact/service_request.html'
    form_class = ServiceRequestForm
    success_url = reverse_lazy('contact:service_request')
    
    def form_valid(self, form):
        # حفظ الطلب
        request_obj = form.save()
        
        # إرسال إشعار بريد إلكتروني
        try:
            send_mail(
                subject=f'طلب خدمة جديد: {request_obj.service.title_ar}',
                message=f'''
                طلب خدمة جديد من: {request_obj.name}
                البريد الإلكتروني: {request_obj.email}
                الهاتف: {request_obj.phone}
                الخدمة المطلوبة: {request_obj.service.title_ar}
                الأولوية: {request_obj.get_priority_display()}
                التاريخ المفضل: {request_obj.preferred_date or 'غير محدد'}
                
                تفاصيل الطلب:
                {request_obj.description}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(self.request, _('تم إرسال طلبك بنجاح. سنتواصل معك قريباً'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('حدث خطأ في إرسال الطلب. يرجى المحاولة مرة أخرى'))
        return super().form_invalid(form)

class AppointmentView(BaseView, FormView):
    """حجز موعد"""
    template_name = 'contact/appointment.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('contact:appointment')
    
    def form_valid(self, form):
        # حفظ طلب الموعد (يستخدم نفس نموذج ServiceRequest)
        appointment = form.save()
        appointment.priority = 'high'  # أولوية عالية للمواعيد
        appointment.save()
        
        # إرسال إشعار بريد إلكتروني
        try:
            send_mail(
                subject=f'طلب موعد جديد: {appointment.service.title_ar}',
                message=f'''
                طلب موعد جديد من: {appointment.name}
                البريد الإلكتروني: {appointment.email}
                الهاتف: {appointment.phone}
                الخدمة: {appointment.service.title_ar}
                التاريخ المطلوب: {appointment.preferred_date}
                
                تفاصيل إضافية:
                {appointment.description}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(self.request, _('تم حجز موعدك بنجاح. سنتواصل معك لتأكيد الموعد'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('حدث خطأ في حجز الموعد. يرجى المحاولة مرة أخرى'))
        return super().form_invalid(form)

class ContactSuccessView(BaseView, TemplateView):
    """صفحة نجاح الإرسال"""
    template_name = 'contact/success.html'
# contact/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import ContactMessage, ServiceRequest
from services.models import Service

class ContactForm(forms.ModelForm):
    """نموذج التواصل"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'contact_type', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('الاسم الكامل')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('رقم الهاتف')}),
            'contact_type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('موضوع الرسالة')}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('نص الرسالة')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6 mb-3'),
                Column('email', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('phone', css_class='col-md-6 mb-3'),
                Column('contact_type', css_class='col-md-6 mb-3'),
            ),
            'subject',
            'message',
            HTML('<div class="text-center mt-3">'),
            Submit('submit', _('إرسال الرسالة'), css_class='btn btn-primary btn-lg px-5'),
            HTML('</div>'),
        )

class ServiceRequestForm(forms.ModelForm):
    """نموذج طلب الخدمة"""
    
    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'phone', 'service', 'description', 'priority', 'preferred_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('الاسم الكامل')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('رقم الهاتف')}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('وصف تفصيلي لطلبك')}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6 mb-3'),
                Column('email', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('phone', css_class='col-md-6 mb-3'),
                Column('service', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('priority', css_class='col-md-6 mb-3'),
                Column('preferred_date', css_class='col-md-6 mb-3'),
            ),
            'description',
            HTML('<div class="text-center mt-3">'),
            Submit('submit', _('إرسال الطلب'), css_class='btn btn-primary btn-lg px-5'),
            HTML('</div>'),
        )

class AppointmentForm(forms.ModelForm):
    """نموذج حجز الموعد"""
    
    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'phone', 'service', 'description', 'preferred_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('الاسم الكامل')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('رقم الهاتف')}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('تفاصيل إضافية عن الموعد')}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['preferred_date'].required = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6 mb-3'),
                Column('email', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('phone', css_class='col-md-6 mb-3'),
                Column('preferred_date', css_class='col-md-6 mb-3'),
            ),
            'service',
            'description',
            HTML('<div class="text-center mt-3">'),
            Submit('submit', _('حجز الموعد'), css_class='btn btn-primary btn-lg px-5'),
            HTML('</div>'),
        )

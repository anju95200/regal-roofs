from django import forms
from ..models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message',
                'cols': 30,
                'rows': 7
            })
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from listings.models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
        }

class UserProfileForm(forms.ModelForm):
    delete_profile_picture = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture', 'delete_profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm new password'})
        # If the user doesn't have a usable password, remove the old password field
        if not user.has_usable_password():
            self.fields.pop('old_password')

    def clean_old_password(self):
        # Skip old password validation if the user doesn't have a password
        if not self.user.has_usable_password():
            return None  # No validation needed
        return super().clean_old_password()

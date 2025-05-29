# face_app/forms.py
from django import forms
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'face_image']

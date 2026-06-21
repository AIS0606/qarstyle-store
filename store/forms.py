from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Order

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Требуется для подтверждения аккаунта.')

    class Meta:
        model = User
        fields = ('username', 'email')

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'payment_method']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (777) 123-45-67'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select form-control'}),
        }

class BodyProfileForm(forms.ModelForm):
    class Meta:
        from .models import BodyProfile
        model = BodyProfile
        fields = ['gender', 'height', 'weight', 'chest', 'waist', 'hips']
        widgets = {
            'gender': forms.Select(attrs={'class': 'zara-input-group', 'style': 'width:100%; border:none; border-bottom: 1px solid #d1d1d1; font-size:11px; text-transform:uppercase; font-family:Inter; padding:10px 0; background:transparent;'}),
            'height': forms.NumberInput(attrs={'class': 'zara-input-group', 'placeholder': ' '}),
            'weight': forms.NumberInput(attrs={'class': 'zara-input-group', 'placeholder': ' '}),
            'chest': forms.NumberInput(attrs={'class': 'zara-input-group', 'placeholder': ' '}),
            'waist': forms.NumberInput(attrs={'class': 'zara-input-group', 'placeholder': ' '}),
            'hips': forms.NumberInput(attrs={'class': 'zara-input-group', 'placeholder': ' '}),
        }

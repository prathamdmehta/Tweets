from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={ 
                'class': 'form-control form-control-lg bg-dark text-light border-info',
                'rows': 4,
                'placeholder': 'What\'s happening?'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-dark text-light border-info'
            }),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
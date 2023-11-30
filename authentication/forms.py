from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='', widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))
    password = forms.CharField(max_length=63, label='',
                               widget=forms.PasswordInput(attrs={
                                   "placeholder": "Mot de passe",
                                   "col": 50,
                                   }
                                ))


class SignupForm(UserCreationForm):
    password1 = forms.CharField(max_length=63, label="", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(max_length=63, label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe'}))
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        help_texts = {
            "username": None,
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
        }
        labels = {
            "username": "",
        }
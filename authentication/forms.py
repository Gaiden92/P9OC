from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """A class represent a login form.

    Arguments:
        forms -- a django form
    """
    username = forms.CharField(
        max_length=63,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
    )
    password = forms.CharField(
        max_length=63,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "col": 50,
            }
        ),
    )


class SignupForm(UserCreationForm):
    """A class represent a signup form.

    Arguments:
        UserCreationForm -- a user creation form
    """
    password1 = forms.CharField(
        max_length=63,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )
    password2 = forms.CharField(
        max_length=63,
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirmer mot de passe"}
            ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        help_texts = {
            "username": None,
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Nom d'utilisateur"}),
        }
        labels = {
            "username": "",
        }

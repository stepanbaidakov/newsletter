from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from .mixins import FormControlMixin
from .models import CustomUser


class CustomUserCreationForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2", "avatar")
        usable_password = None


class CustomLoginForm(FormControlMixin, AuthenticationForm):
    pass


class CustomUserChangeForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "avatar")


class CustomPasswordResetForm(FormControlMixin, PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(FormControlMixin, SetPasswordForm):
    pass

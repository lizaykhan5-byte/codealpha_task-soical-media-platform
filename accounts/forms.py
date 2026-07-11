from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

import re

from .models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter username",
            "autocomplete": "username",
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email",
            "autocomplete": "email",
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter strong password",
            "autocomplete": "new-password",
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password",
            "autocomplete": "new-password",
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()

        if len(username) < 3:
            raise ValidationError(
                "Username must be at least 3 characters."
            )

        if " " in username:
            raise ValidationError(
                "Username cannot contain spaces."
            )

        if not re.fullmatch(r"[A-Za-z0-9_.]+", username):
            raise ValidationError(
                "Username can only contain letters, numbers, underscores, and dots."
            )

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                "Username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "Email already registered."
            )

        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1", "")

        if len(password) < 8:
            raise ValidationError(
                "Password must be at least 8 characters."
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(
                "Password must contain at least one special character."
            )

        return password

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            "autocomplete": "current-password",
        })
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Your account is not verified yet. Please check your email "
                "inbox and spam folder.",
                code="inactive",
            )


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
        })
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()

        existing_user = User.objects.filter(
            username__iexact=username
        ).exclude(pk=self.instance.pk)

        if existing_user.exists():
            raise ValidationError(
                "Username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        existing_user = User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk)

        if existing_user.exists():
            raise ValidationError(
                "Email already registered."
            )

        return email


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "accept": "image/*",
        })
    )

    cover_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "accept": "image/*",
        })
    )

    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Write something about yourself...",
            "rows": 3,
        })
    )

    location = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your location",
        })
    )

    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "https://yourwebsite.com",
        })
    )

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "cover_photo",
            "bio",
            "location",
            "website",
        ]
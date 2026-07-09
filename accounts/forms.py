from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter username"
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter strong password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exists.")

        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered.")

        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control"
    }))

    cover_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control"
    }))

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Write something about yourself...",
        "rows": 3
    }))

    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Your location"
    }))

    website = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "class": "form-control",
        "placeholder": "https://yourwebsite.com"
    }))

    class Meta:
        model = Profile
        fields = ["profile_picture", "cover_photo", "bio", "location", "website"]
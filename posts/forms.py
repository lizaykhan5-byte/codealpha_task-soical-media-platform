from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': "What's on your mind?",
        'rows': 3
    }))

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Post
        fields = ['caption', 'image']


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write a comment...'
    }))

    class Meta:
        model = Comment
        fields = ['text']
from django import forms
from django.forms import ModelForm

from .models import Post


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["user", "modified_at", "created_at", "solved_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }

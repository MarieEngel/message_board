from django import forms
from django.forms import ModelForm

from .models import Post, Comment, Category


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["user", "modified_at", "created_at", "solved_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class SearchForm(forms.Form):
    # query = forms.CharField(label="Search term", max_length=50)
    cat = [(c.name, c.name) for c in Category.objects.all()]
    categories = forms.ChoiceField(widget=forms.Select, choices=cat, required=False, label='')
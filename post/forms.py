from django import forms

from .models import Post, Comment, Category


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["user", "modified_at", "created_at", "solved_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(attrs={"class": "form-control latitude"}),
            "longitude": forms.HiddenInput(attrs={"class": "form-control longitude"}),
            "postcode": forms.HiddenInput(attrs={"class": "form-control postcode"}),
            "city": forms.HiddenInput(attrs={"class": "form-control city"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class SearchForm(forms.Form):
    categories = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "select-category",
            }
        ),
        choices=[("All", "All")],
        required=False,
        label="",
    )
    query = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Search", "class": "form-control me-2"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = self.fields.get("categories")
        categories.choices = categories.choices + [
            (c.name, c.name) for c in Category.objects.all()
        ]

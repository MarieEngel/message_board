from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ["user"]
        widgets = {
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(attrs={"class": "form-control latitude"}),
            "longitude": forms.HiddenInput(attrs={"class": "form-control longitude"}),
            "city": forms.TextInput(attrs={"class": "form-control city"}),
            "postcode": forms.TextInput(attrs={"class": "form-control postcode"}),
            "street": forms.TextInput(attrs={"class": "form-control street"}),
            "street_number": forms.NumberInput(
                attrs={"class": "form-control street_number"}
            ),
        }


# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

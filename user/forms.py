from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ["user"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(attrs={"class": "form-control latitude"}),
            "longitude": forms.HiddenInput(attrs={"class": "form-control longitude"}),
        }


# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


# Create a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["image"]

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_postcode(value):
    if value != "8305":
        raise ValidationError("Only people from island Samsø can register")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics", blank=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    postcode = models.CharField(max_length=8, validators=[validate_postcode])
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100, null=True, blank=True)
    street_number = models.PositiveIntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return f"Profile(user={self.user.username})"

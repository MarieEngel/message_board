from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    postcode = models.CharField(max_length=8)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100, null=True, blank=True)
    street_number = models.PositiveIntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return f"Profile(user={self.user.username})"

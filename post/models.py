from django.db import models
from django.contrib.auth.models import User

# class Location(models.Model):
#     street = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=4)

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __repr__(self) -> str:
        return f'Category(name={self.name})'


class Post(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True, upload_to="images/")
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    solved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.post.title, self.user.username)

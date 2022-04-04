from django.db import models
from django.contrib.auth.models import User

# class Location(models.Model):
#     street = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=4)


class Post(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True, upload_to="images/")
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # location = models.OneToOneField(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    solved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user}"



class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return 'Comment by {}'.format(self.name)    






    
    

    
    
   
   

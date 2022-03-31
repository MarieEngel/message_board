from django.db import models

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return '%s - %s' % (self.post.title, self.name)

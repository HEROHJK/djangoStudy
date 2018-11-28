from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    writer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    postIndex = models.ForeignKey('Post', on_delete=models.CASCADE)
    writer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
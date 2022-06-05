from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    description = models.CharField(max_length = 255, blank = True)
    pic = models.ImageField(default='default.jpg',upload_to='images/')
    date_posted = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='posts',
        null=True, blank = True, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('posts:post-detail',kwargs={'pk':self.pk})

class Comment(models.Model):
    Post = models.ForeignKey(Post, related_name='comments',
        on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='comments',
        null=True, blank = True, on_delete=models.CASCADE)
    message = models.CharField(max_length = 255, blank = False)
    # difference between auto_now & timezone.now :
    # default = timezone.now means user can edit the date of creation while making
    # comment while auto_now = True means user doesn't have control and it will be
    # the date of saving of comment by default
    date = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes',
        null=True, blank = True, on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, related_name='likes',
        on_delete = models.CASCADE)

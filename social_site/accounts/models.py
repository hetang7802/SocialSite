from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pic')
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length = 100, blank = True)
    friends = models.ManyToManyField('Profile',blank = True)

    def __str__(self):
        return f'@{self.user.username}'

    def get_absolute_url(self):
        return "users/{}".format(self.slug)


def post_save_user_model_receiver(sender,instance,created,*args,**kwargs):
    if(created):
        try:
            Profile.objects.update(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)

class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "from {} to {}".format(self.from_user.username, self.to_user.username)

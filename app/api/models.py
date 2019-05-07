from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string  

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return(self.user.username)

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    account = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.now)
    views = models.IntegerField(default=0)
    size = models.CharField(default='small', max_length=10)
    slug = models.SlugField(max_length=5, blank=True)
    profile = models.ForeignKey(Profile, related_name='userposts', default=1, on_delete=models.CASCADE)
    def __str__(self):
        return(self.title)
    def save(self, *args, **kwargs):
        slug_save(self) # call slug_save, listed below
        super(Post, self).save(*args, **kwargs)

def slug_save(obj):
  #A function to generate a 5 character slug and see if it has been used
  if not obj.slug: # if there isn't a slug
    obj.slug = get_random_string(5) # create one
    slug_is_wrong = True  
    while slug_is_wrong: # keep checking until we have a valid slug
        slug_is_wrong = False
        other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
        if len(other_objs_with_slug) > 0:
            # if any other objects have current slug
            slug_is_wrong = True
        if slug_is_wrong:
            # create another slug and check it again
            obj.slug = get_random_string(5)
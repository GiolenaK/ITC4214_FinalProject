from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)  #when a user is saved, send the signal
#the receiver is the create_profile function
def create_profile(sender, instance, created, **kwargs):  #kwargs accepts any other keyword arguments
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserManager,User
from drc.apps.profiles.models import Profile

@receiver(post_save, sender=User)#settings.AUTH_USER_MODEL)
def create_related_profile(sender, instance, created, *args, **kwargs):

    print('create_related_profile',instance)

    if instance and created:
        instance.profile = Profile.objects.create(user=instance)

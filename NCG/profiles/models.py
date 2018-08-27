from django.db import models

# importing this for use with user profiles:
from django.contrib.auth.models import User

# these allow django to create/update 'Profiles' instances automatically
# when we create/update User instances:
from django.db.models.signals import post_save
from django.dispatch import receiver

# states used as options in the profile model:
from .states import states_list


# Create your models here.



class Profile(models.Model):
	user		= models.OneToOneField(User, on_delete=models.CASCADE)
	phone		= models.CharField(max_length=30, blank=True)
	address1	= models.CharField(max_length=30, blank=False)
	address2	= models.CharField(max_length=30, blank=True)
	city		= models.CharField(max_length=30, blank=False)
	state		= models.CharField(max_length=30, blank=False, choices=states_list)
	zip			= models.CharField(max_length=30, blank=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	profile_picture = models.ImageField(max_length=255, upload_to='profile_pictures/',
		default = 'profile_pictures/default.png')
	phone_number = models.CharField(max_length = 11, null = False, blank = False)
	first_name = models.CharField(max_length=30, null=False, blank=False)
	last_name = models.CharField(max_length=30, null = False, blank = False)
	date_created = models.DateTimeField(auto_now_add= True)
	
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


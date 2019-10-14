from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    TRAVEL_STYLE = (
        ('FOODIE','Foodie'),
        ('LUX','Lux'),
        ('BUDGET','Budget'),
        ('SOLO','Solo'),
        ('HOTEL','Hotel'),
        ('FAMILY','Family'),
        ('WORK','Work'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    travel_style = models.CharField(max_length=20, choices=TRAVEL_STYLE)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



    
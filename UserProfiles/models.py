import os
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

class Profile(models.Model):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    AGE_DEMOGRAPHIC = (
        ('UNDER 12','Under 12 years old'),
        ('12-17','12-17 years old'),
        ('18-24','18-24 years old'),
        ('25-34','25-34 years old'),
        ('35-44','35-44 years old'),
        ('45-54','45-54 years old'),
        ('55-64','55-64 years old'),
        ('65-74','65-74 years old'),
        ('OVER 75','75 years or older'),
    )
    TRAVEL_FREQUENCY = (
        ('1 OR LESS','One trip or less'),
        ('1 TO 3','1-3 trips'),
        ('4 TO 8','4-8 trips'),
        ('8 TO 12','8-12 trips'),
        ('12 OR MORE','12 or more trips'),
    )
    TRAVEL_STYLE = (
        ('FOODIE','Foodie'),
        ('LUX','Lux'),
        ('BUDGET','Budget'),
        ('SOLO','Solo'),
        ('HOTEL','Hotel'),
        ('FAMILY','Family'),
        ('WORK','Work'),
    )
    TRIP_LENGTH = (
        ('LESS THAN ONE WEEK','Less than a week'),
        ('1 TO 2 WEEKS','1-2 weeks'),
        ('3 TO 4 WEEKS','3-4 weeks'),
        ('1 TO 3 MONTHS','1-3 months'),
        ('3 TO 6 MONTHS','3-6 months'),
        ('MORE THAN 6 MONTHS', '<6 months: I got no roots!')
    )
    AVERAGE_COST = (
        ('LESS THAN 5000','Less than $5,000'),
        ('5000 TO 10000','Between $5,000 and $10,000'),
        ('MORE THAN 10000','More than $10,000'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default1.jpg', upload_to='profile_pics/', null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    travel_style = models.CharField(max_length=20, choices=TRAVEL_STYLE, null=True, blank=True)

    #Social Accounts
    nerd = models.BooleanField(choices=TRUE_FALSE_CHOICES, null=True, blank=True)
    facebook_url = models.URLField(max_length=150, null=True, blank=True)
    instagram_url = models.URLField(max_length=150, null=True, blank=True)
    tiktok_url = models.URLField(max_length=150, null=True, blank=True)

    home_airport = models.CharField(max_length=3, null=True, blank=True)
    age_bracket = models.CharField(max_length=50, choices=AGE_DEMOGRAPHIC, null=True, blank=True)
    int_travel = models.CharField(max_length=50, choices=TRAVEL_FREQUENCY, null=True, blank=True)
    dom_travel = models.CharField(max_length=50, choices=TRAVEL_FREQUENCY, null=True, blank=True)
    average_length = models.CharField(max_length=50, choices=TRIP_LENGTH, null=True, blank=True)
    average_cost = models.CharField(max_length=50, choices=AVERAGE_COST, null=True, blank=True)

    

    



    # signup_confirmation = models.BooleanField(default=False)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


def get_image_filename(instance, filename):
    
    #id = instance.post.id
    return os.path.join("gallery_pics/%s/" % instance.profile.user.username, filename) 

class Images(models.Model):
    profile = models.ForeignKey(Profile, related_name="photos", default=None, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=get_image_filename, blank=True, null=True)
    
    def __str__(self):
        return self.image.url
    
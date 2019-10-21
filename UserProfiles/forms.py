
from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Images
from django.forms.models import modelformset_factory

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name',
            'last_name',
            'password1', 
            'password2'
            ]

#https://www.youtube.com/watch?v=Tja4I_rgspI

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email',
            ]

class ProfileRegisterForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    """
    TRAVEL_STYLE = (
        ('FOODIE','Foodie'),
        ('LUX','Lux'),
        ('BUDGET','Budget'),
        ('SOLO','Solo'),
        ('HOTEL','Hotel'),
        ('FAMILY','Family'),
        ('WORK','Work'),
    )
    """
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

    glter = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label='Are you a part of the Girls love travel Facebook group?')
    facebook_url = forms.CharField(max_length=150, label='Facebook URL (if applicable)')
    home_airport = forms.CharField(max_length=3,label='What is the three letter code for your home airport?')
    age_bracket = forms.ChoiceField(choices=AGE_DEMOGRAPHIC, label='What is your age bracket?')
    class Meta:
        model = Profile
        fields =[
            'bio', 
            'location', 
            'travel_style', 
            'glter',
            'facebook_url',
            'home_airport',
            'age_bracket',
            ]

class PostRegUpdateForm(forms.ModelForm):
    TRAVEL_FREQUENCY = (
        ('1 OR LESS','One trip or less'),
        ('1 TO 3','1-3 trips'),
        ('4 TO 8','4-8 trips'),
        ('8 TO 12','8-12 trips'),
        ('12 OR MORE','12 or more trips'),
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
    int_travel = forms.ChoiceField(choices=TRAVEL_FREQUENCY, label='How often do you travel internationally each year?')
    dom_travel = forms.ChoiceField(choices=TRAVEL_FREQUENCY, label='How often do you travel domestically each year?')
    average_length = forms.ChoiceField(choices=TRIP_LENGTH, label='What is the length of your average holiday?')
    average_cost = forms.ChoiceField(choices=AVERAGE_COST, label="On average, how much do you spend on a trip?")
    class Meta:
        model = Profile
        fields =[
            'avatar',
            'int_travel',
            'dom_travel',
            'average_length',
            'average_cost',
            
            ]

         
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )


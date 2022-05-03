from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse
from django.utils.safestring import mark_safe


gender = (
        ('Male','Male'),
        ('Female','Female'),
        )


class User(models.Model):
    username = models.CharField(max_length=500, verbose_name="User Name", unique=True )
    firstName = models.CharField(max_length=500, verbose_name="First Name", blank=True)
    lastName = models.CharField(max_length=500, verbose_name="Last Name", blank=True)
    gender =  models.CharField(choices=gender,   max_length=100, verbose_name="Gender", blank=True, default='Male')
    phoneValidator = RegexValidator(regex=r'^\+?1?\d{10,15}$',message='Please enter your phonenumber in the format starting with: 09 or +251',)
    phoneNumber = models.CharField(validators=[phoneValidator], max_length=15, blank=True, verbose_name="Phone Number")
    profilePicture = models.ImageField(upload_to='Profile_Pictures/', default='Profile_Pictures/default.png', verbose_name="Profile Picture")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="last login")
    is_active = models.BooleanField(default=True)
    counter = models.IntegerField(default=0, blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    

    USERNAME_FIELD = 'username'





    # def get_absolute_url(self):
    #     return reverse('ro-profile', kwargs={'pk' : self.pk})





    def __str__(self):
        return self.username



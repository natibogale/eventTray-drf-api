
from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField

from authentication.models import *





class profileUpdateForm(forms.ModelForm):



    # phoneValidator = RegexValidator(
    #     regex=r"^\+?1?\d{10}$",
    #     message="Please enter your phonenumber in the format starting with: 09",
    # )
    # phoneNumber = forms.CharField(
    #     validators=[phoneValidator],
    #     max_length=10,
    #     label="",
    #     widget=forms.TextInput()        
    # ) 



    class Meta:
        model = User
        fields = ('username','firstName','lastName','phoneNumber','email','profilePicture','coverPicture')
from django.contrib.auth import authenticate
from django import forms
from .models import *


class loginForm(forms.Form):
    phoneValidator = RegexValidator(
        regex=r"^\+?1?\d{10}$",
        message="Please enter your phonenumber in the format starting with: 09",
    )
    phoneNumber = forms.CharField(
        validators=[phoneValidator],
        max_length=10,
        label=" ",
        
    ) 
    # class Meta:
    #     model = User
    #     fields = ('phoneNumber',)
    
    # def __init__(self, *args, **kwargs):
    #     super(loginForm, self).__init__(*args, **kwargs)
    #     self.fields['phoneNumber'].label = " "
    
    # def clean(self):
    #     if self.is_valid():
    #         username = self.cleaned_data['username']
    #         password = self.cleaned_data['password']
    #         if not authenticate(username=username, password=password):
    #             raise forms.ValidationError("Invalid Login")
            
      
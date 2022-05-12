from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField


class loginForm(forms.Form):
    phoneValidator = RegexValidator(
        regex=r"^\+?1?\d{10}$",
        message="Please enter your phonenumber in the format starting with: 09",
    )
    phoneNumber = forms.CharField(
        validators=[phoneValidator],
        max_length=10,
        label="",
        widget=forms.TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"Phone Number 09- Format", "class": "input-field" })        
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
            


class registrationForm(forms.ModelForm):

    roles = (
        ("User", "User"),
        ("Organizer", "Organizer"),
        ("Checker", "Checker"),
    )

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
    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    role = forms.CharField(widget=forms.HiddenInput(), required=False)

    


    class Meta:
        model = User
        fields = ('username','firstName','lastName','phoneNumber','email','role','password')

        widgets = {
            'username': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"Username", "class": "input-field"}),
            'firstName': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"First Name", "class": "input-field"}),
            'lastName': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"Last Name", "class": "input-field"}),
            'email': TextInput(attrs={'type': 'email', 'autocomplete':"off", "placeholder":"Email", "class": "input-field"}),
            'role': TextInput(attrs={'type': 'select' ,"label":"None",'autocomplete':"off", "placeholder":"Role", "class": "input-field"}),
            'phoneNumber': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"Phone Number 09- Format", "class": "input-field" })
        }
        labels = {
            'username': "",
            "firstName":"",
            "lastName":"",
            "email":"",
            "role":"",
            "phoneNumber": ""

        }





class otpForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        label="",
    widget=forms.TextInput(attrs={'type': 'text', 'onfocus':"setCursorInputPosition(this, this.value.length);", 'minlength': 6, 'autocomplete':"off", "class": "input-field middle" })        
    ) 
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
            # 'role': TextInput(attrs={'type': 'select' ,"label":"None",'autocomplete':"off", "placeholder":"Role", "class": "input-field"}),
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
        help_texts = {
            'username': 'If you are an organization, put the name under the business license for First and Last Name!',

        }




class otpForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        label="",
    widget=forms.TextInput(attrs={'type': 'text', 'onfocus':"setCursorInputPosition(this, this.value.length);", 'minlength': 6, 'autocomplete':"off", "class": "input-field middle" })        
    ) 







class organizerForm(forms.ModelForm):

    # organizer = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Organizer
        fields = ('displayName','organizerType','twitter','telegram','facebook','instagram')


    # organizer = forms.ChoiceField(choices = [])
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(organizerForm, self).__init__(*args, **kwargs)
    #     self.fields['organizer'].choices = [(x.pk,x.firstName+" "+x.lastName) for x in User.objects.filter(id=user)]

    
        # widgets = {
        #     'email': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"Username", "class": "input-field"}),
        #     'displayName': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"First Name", "class": "input-field"}),
        #     'twitter': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"You can leave this field empty", "class": "input-field"}),
        #     'telegram': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"You can leave this field empty", "class": "input-field"}),
        #     'facebook': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"You can leave this field empty", "class": "input-field" }),
        #     'instagram': TextInput(attrs={'type': 'text', 'autocomplete':"off", "placeholder":"You can leave this field empty", "class": "input-field" })

        # }
    #     labels = {
    #         'username': "",
    #         "firstName":"",
    #         "lastName":"",
    #         "email":"",
    #         "role":"",
    #         "phoneNumber": ""

    #     }
    #     help_texts = {
    #         'username': 'If you are an organization, put the name under the business license for First and Last Name!',

    #     }
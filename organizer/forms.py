
from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField
from .forms import *

from authentication.models import *



class DateInput(forms.DateInput):
    input_type = 'date'



class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','firstName','lastName','phoneNumber','email','profilePicture','coverPicture')




class organizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ('displayName','organizerType','twitter','telegram','facebook','instagram')


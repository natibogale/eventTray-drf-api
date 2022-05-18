from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField

from authentication.models import *
from ckeditor.widgets import CKEditorWidget


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TextInput):
    input_type = "time"


class createEventForm(forms.ModelForm):


    eventStartDate = forms.DateField(label = "Event Starts on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )
    eventEndDate = forms.DateField(label = "Event Ends on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )
    eventStartTime = forms.TimeField(label= "Event starts at", 
        widget=forms.TimeInput(attrs={"type": "time"})
    )
    eventEndTime = forms.TimeField(label= "Event ends at",
        widget=forms.TimeInput(attrs={ "type": "time"})
    )

    class Meta:
        model = Events
        fields = (
            "eventName",
            "eventDescription",
            "payment",
            "eventCategories",
            "eventStartDate",
            "eventEndDate",
            "eventStartTime",
            "eventEndTime",
            "eventLocation",
            "eventType",
            "venue",
            "eventCity",
        )

    widgets = {
        # 'eventStartDate': DateInput(attrs={'class':'form-control', 'type':'date'}),
        # 'eventEndDate':DateInput(attrs={'class':'form-control', 'type':'date'}),
        # 'eventStartTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
        # 'eventEndTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
        "eventDescription": CKEditorWidget(),
    }
    labels = {
        'eventStartDate': "Event Starts on",
        'eventEndDate':"Event Ends on",
        'eventStartTime':"Event starts at",
        'eventEndTime':"Event ends at",
        
    }



class ImagesForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ('image',)
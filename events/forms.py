from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField

from authentication.models import *
from ckeditor.widgets import CKEditorWidget

from datetime import datetime,date

class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TextInput):
    input_type = "time"


class createEventForm(forms.ModelForm):


    eventStartDate = forms.DateField(label = "Event Starts on",
        widget=forms.DateInput(attrs={ "type": "date", 'class':'mt-2'})
    )
    eventEndDate = forms.DateField(label = "Event Ends on",
        widget=forms.DateInput(attrs={ "type": "date", 'class':'mt-2'})
    )
    eventStartTime = forms.TimeField(label= "Event starts at", 
        widget=forms.TimeInput(attrs={"type": "time", 'class':'mt-2'})
    )
    eventEndTime = forms.TimeField(label= "Event ends at",
        widget=forms.TimeInput(attrs={ "type": "time", 'class':'mt-2'})
    )
    eventLocation = forms.CharField( label="Event Location",
        widget = forms.TextInput(attrs={'id':'location', 'class':'readonly', 'placeholder':'Choose location from map', 'autocomplete':'off'})
    )
    venue = forms.CharField( label="Venue",
        widget = forms.TextInput(attrs={'type':'text', 'placeholder':'Choose from existing or Input your own','list':'selectVenue', 'autocomplete':'off'})
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
            "eventType",
            "eventCity",
            "venue",
            "eventLocation",

        )

        widgets = {
            # 'eventStartDate': DateInput(attrs={'class':'form-control', 'type':'date'}),
            # 'eventEndDate':DateInput(attrs={'class':'form-control', 'type':'date'}),
            # 'eventStartTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
            # 'eventEndTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
            # "eventDescription": CKEditorWidget(),
            # "eventLocation" : TextInput(attrs={'id':'location', 'class':'readonly', 'placeholder':'Choose location from map', 'autocomplete':'off'}),
            # "venue":forms.HiddenInput(),

            
        }
 
    
    # def __init__(self, *args, **kwargs):
    #     super(createEventForm, self).__init__(*args, **kwargs)
    #     self.fields['directorate'].required = True
    #     self.fields['team'].required = True

    def clean(self):
        # Get the user submitted names from the cleaned_data dictionary
        cleaned_data = super().clean()
        startDate = cleaned_data.get('eventStartDate')
        endDate = cleaned_data.get('eventEndDate')
        if endDate < startDate:
            raise forms.ValidationError("An Event cannot end before it's start date!")
            
        if startDate < date.today():
            raise ValidationError("Start Date cannot be in the past")  

        return cleaned_data

    # def clean_eventEndTime(self):
    #     startTime = self.cleaned_data['eventStartTime']
    #     endTime = self.cleaned_data['eventEndTime']
    #     if startTime < endTime:
    #         raise forms.ValidationError("An Event cannot end before it's starting time!")
    #     return endTime

class ImagesForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ('image',)





class updateEventForm(forms.ModelForm):

    eventStartDate = forms.DateField(label = "Event Starts on",
        widget=forms.DateInput(attrs={ "type": "date", 'class':'mt-2'})
    )
    eventEndDate = forms.DateField(label = "Event Ends on",
        widget=forms.DateInput(attrs={ "type": "date", 'class':'mt-2'})
    )
    eventStartTime = forms.TimeField(label= "Event starts at", 
        widget=forms.TimeInput(attrs={"type": "time", 'class':'mt-2'})
    )
    eventEndTime = forms.TimeField(label= "Event ends at",
        widget=forms.TimeInput(attrs={ "type": "time", 'class':'mt-2'})
    )
    eventLocation = forms.CharField( label="Event Location",
        widget = forms.TextInput(attrs={'id':'location', 'class':'readonly', 'placeholder':'Choose location from map', 'autocomplete':'off'})
    )
    venue = forms.CharField( label="Venue",
        widget = forms.TextInput(attrs={'type':'text', 'placeholder':'Choose from existing or Input your own','list':'selectVenue', 'autocomplete':'off'})
    )
    class Meta:
        model = Events
        fields = (
            "eventName",
            "eventDescription",
            "eventCategories",
            "eventStartDate",
            "eventEndDate",
            "eventStartTime",
            "eventEndTime",
            "eventType",
            "eventCity",
            "venue",
            "eventLocation",

        )

        widgets = {
            # 'eventStartDate': DateInput(attrs={'class':'form-control', 'type':'date'}),
            # 'eventEndDate':DateInput(attrs={'class':'form-control', 'type':'date'}),
            # 'eventStartTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
            # 'eventEndTime':TimeInput(attrs={'class':'form-control', 'type':'time'}),
            # "eventDescription": CKEditorWidget(),
            # "eventLocation" : TextInput(attrs={'id':'location', 'class':'readonly', 'placeholder':'Choose location from map', 'autocomplete':'off'}),
            # "venue":forms.HiddenInput(),
        }
 
    
    # def __init__(self, *args, **kwargs):
    #     super(createEventForm, self).__init__(*args, **kwargs)
    #     self.fields['directorate'].required = True
    #     self.fields['team'].required = True


    def clean(self):
        # Get the user submitted names from the cleaned_data dictionary
        cleaned_data = super().clean()
        startDate = cleaned_data.get('eventStartDate')
        endDate = cleaned_data.get('eventEndDate')
        if endDate < startDate:
            raise forms.ValidationError("An Event cannot end before it's start date!")
            
        if startDate < date.today():
            raise ValidationError("Start Date cannot be in the past")  
                      
        return cleaned_data
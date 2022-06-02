from django.contrib.auth import authenticate
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, EmailField

from authentication.models import *
from ckeditor.widgets import CKEditorWidget
from events.models import *







class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TextInput):
    input_type = "time"




class createEventTicketForm(forms.ModelForm):
    # def clean(self):
    #     # Get the user submitted names from the cleaned_data dictionary
    #     cleaned_data = super().clean()
    #     event = cleaned_data.get("event")
    #     ticketName = cleaned_data.get("ticketName")
    #     ticketName = cleaned_data.get("ticketName")
    #     ticketName = cleaned_data.get("ticketName")
    #     ticketName = cleaned_data.get("ticketName")
    #     ticketName = cleaned_data.get("ticketName")


    #     last_name = cleaned_data.get("last_name")

    #     # Check if the first letter of both names is the same
    #     if first_name[0].lower() != last_name[0].lower():
    #         # If not, raise an error
    #         raise ValidationError("The first letters of the names do not match")

    #     return cleaned_data

    startSaleOn = forms.DateField(label = "Start Ticket Sale on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )
    endSaleOn = forms.DateField(label = "End Ticket Sale on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )
    ticketName = forms.CharField( label="Ticket Name",
        widget = forms.TextInput(attrs={'type':'text', 'placeholder':'Choose a name for your ticket','list':'selectTicketName', 'autocomplete':'off'})
    )
    class Meta:
        model = Tickets
        fields = (
            "event",
            "ticketName",
            "ticketDescription",
            "quantity",
            "price",
            "ticketPerUser",
            "startSaleOn",
            "endSaleOn",
        )

    labels = {
        'startSaleOn': "Start Ticket Sale on",
        'endSaleOn':"End Ticket Sale on",
        
    }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset=Events.objects.filter(organizer=user, expired=False)
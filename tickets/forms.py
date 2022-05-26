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




class createEventTicketForm(forms.ModelForm):

    startSaleOn = forms.DateField(label = "Start Ticket Sale on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )
    endSaleOn = forms.DateField(label = "End Ticket Sale on",
        widget=forms.DateInput(attrs={ "type": "date"})
    )

    class Meta:
        model = Events
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

from django.db import models
from django.core.exceptions import ValidationError

# from ckeditor import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from location_field.models.plain import PlainLocationField

# Create your models here.
from PIL import Image

from django.conf import settings
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator




class Tickets(models.Model):
    ticketOwner =  models.ForeignKey("authentication.User", verbose_name="Ticket Owner", on_delete=models.CASCADE) 
    event  = models.ForeignKey("events.Events", verbose_name="Event", on_delete=models.CASCADE)    
    ticketName  = models.CharField(max_length = 150, verbose_name="Ticket Name")
    ticketDescription = models.TextField(verbose_name="Ticket Description",blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.FloatField(verbose_name="Price per Unit", default=0,validators=[MinValueValidator(0.0)])
    ticketPerUser = models.PositiveIntegerField(verbose_name="Ticket Sell per User")
    soldTickets = models.PositiveIntegerField(verbose_name="Sold Tickets", blank=True, null=True)
    startSaleOn = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Start Sale on" )
    endSaleOn = models.DateField(auto_now=False, auto_now_add=False, verbose_name="End Sale on" )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = ("Tickets")

    def __str__(self):
        return self.ticketName


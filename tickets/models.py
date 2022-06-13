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

import uuid



class Tickets(models.Model):
    ticketOwner =  models.ForeignKey("authentication.User", verbose_name="Ticket Owner", on_delete=models.CASCADE) 
    event  = models.ForeignKey("events.Events", verbose_name="Event", on_delete=models.CASCADE)    
    eventName = models.CharField(max_length=100, verbose_name="Event Name", blank=True, null=True)
    ticketName  = models.CharField(max_length = 150, verbose_name="Ticket Name")
    ticketDescription = models.TextField(verbose_name="Ticket Description",blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.FloatField(verbose_name="Price per Unit", default=0,validators=[MinValueValidator(0.0)])
    ticketPerUser = models.PositiveIntegerField(verbose_name="Ticket Sell per User", blank=True, null=True)
    soldTickets = models.PositiveIntegerField(verbose_name="Sold Tickets", default=0, blank=True, null=True)
    startSaleOn = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Start Sale on" )
    endSaleOn = models.DateField(auto_now=False, auto_now_add=False, verbose_name="End Sale on" )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = ("Tickets")

    def __str__(self):
        return self.ticketName






class TicketsBought (models.Model):
    ticket = models.ForeignKey("tickets.Tickets", verbose_name="Ticket", on_delete=models.CASCADE)
    ticketName = models.CharField(max_length=100, verbose_name="Ticket Name", blank=True, null=True)
    event = models.ForeignKey("events.Events", verbose_name=("Event"), on_delete=models.CASCADE)
    eventName = models.CharField(max_length=100, verbose_name="Event Name", blank=True, null=True)
    phoneNumber = models.CharField(verbose_name=("Buyer Phone"), max_length=50)
    orderNo = models.CharField(verbose_name=("Order Number"), max_length=50)
    buyer = models.ForeignKey("authentication.User", verbose_name=("Buyer"), on_delete=models.CASCADE)
    buyerName = models.CharField(verbose_name=("Buyer Name"), blank=True, null=True, max_length=50)
    qrCode = models.CharField(max_length=50,verbose_name=("QR Code"), default = uuid.uuid4)
    price = models.CharField(verbose_name=("Price"), max_length=50, blank=True, null=True)
    is_payed = models.BooleanField(default=False)
    is_scanned = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", default=0)
    image = models.ImageField(upload_to='merchs/', blank=True, null=True)
    datePuchased = models.DateField(auto_now=False, auto_now_add=True, verbose_name="Date Purchased") 
    class Meta:
        verbose_name_plural = ("Tickets Bought")

    def __str__(self):
        return self.orderNo



# class TicketHistory(models.Model):
#     orderNo = models.CharField(verbose_name=("Order Number"), max_length=50)
#     phoneNumber = models.CharField(verbose_name=("Buyer Phone"), max_length=50)
#     quantity = models.PositiveIntegerField(verbose_name="Quantity")


#     class Meta:
#         verbose_name_plural = ("Tickets History")

#     def __str__(self):
#         return self.orderNo
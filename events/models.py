from django.db import models

# from ckeditor import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from location_field.models.plain import PlainLocationField

# Create your models here.


from multiselectfield import MultiSelectField

# ...

CATEGORIES = (

    ("Activities", "Activities"),
    ("Art", "Art"),
    ("Bazar", "Bazar"),
    ("Business", "Business"),
    ("Concert", "Concert"),
    ("Conference", "Conference"),
    ("Dance", "Dance"),
    ("Education", "Education"),
    ("Exhibition", "Exhibition"),
    ("Expo", "Expo"),
    ("Fashion", "Fashion"),
    ("Festival", "Festival"),
    ("Film", "Film"),
    ("Food", "Food"),
    ("Fundraiser", "Fundraiser"),
    ("Music", "Music"),
    ("Online Webinar", "Online Webinar"),
    ("Night Life", "Night Life"),
    ("Sports", "Sports"),
    ("Technology", "Technology"),
    ("Travel", "Travel"),
    ("Training", "Training"),
    
)

types = (("In Person", "In Person"), ("Online", "Online"))






class Venues(models.Model):
    venue = models.CharField(verbose_name="Venue", max_length=250)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(  upload_to="Venue Image/",
        verbose_name="Venue Image",)


    class Meta:
        verbose_name_plural = "Venues"

    def __str__(self):
        return self.venue



class Events(models.Model):
    organizer = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    eventName = models.CharField(verbose_name="Event Name", max_length=250)
    eventDescription = RichTextUploadingField(
        config_name="portal_config", verbose_name="Event Description"
    )
    # eventCategory = models.
    eventCategory = MultiSelectField(choices=CATEGORIES, verbose_name="Event Category")
    eventStartDate = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="Event Start Date"
    )
    eventEndDate = models.DateField(
        verbose_name="Event End Date", auto_now=False, auto_now_add=False
    )
    eventStartTime = models.TimeField(
        verbose_name="Event Start Time", auto_now=False, auto_now_add=False
    )
    eventEndTime = models.TimeField(
        verbose_name="Event End Time", auto_now=False, auto_now_add=False
    )
    eventLocation = PlainLocationField(
        based_fields=["city"],
        zoom=7,
        verbose_name="Event Location",
        blank=True,
        null=True,
    )
    eventType = models.CharField(choices=types, verbose_name="Event Type", max_length=250)
    venue = models.CharField(verbose_name="Venue", max_length=250)
    eventCity = models.CharField(verbose_name="Event City", max_length=250)
    eventCountry = models.CharField(verbose_name="Event Country", default="Ethiopia", max_length=250)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)



    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.eventName

    # def get_absolute_url(self):
    #     erse("_detail", kwargs={"pk": self.pk})

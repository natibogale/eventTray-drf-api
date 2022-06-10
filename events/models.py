from django.db import models
from django.core.exceptions import ValidationError

# from ckeditor import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from location_field.models.plain import PlainLocationField

# Create your models here.
from PIL import Image

from django.conf import settings
from multiselectfield import MultiSelectField

# ...


def validate_image(value):
    filesize = value.size
    if filesize > 10485760:
        raise ValidationError("The maximum size that can be uploaded is 10MB")
    import os

    ext = os.path.splitext(value.name)[1]
    ext = ext.split(".")[1]
    if settings.DEBUG:
        if not ext in settings.IMAGE_EXT:
            raise ValidationError(
                "File type not supported! Please upload only:  .jpg, .jpeg, .png format files."
            )


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


PAID = (("Paid", "Paid"), ("Free", "Free"))


class Cities(models.Model):
    city = models.CharField(verbose_name="City", max_length=150)
    country = models.CharField(
        verbose_name="Country", default="Ethiopia", max_length=150
    )

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city


class Venues(models.Model):
    venue = models.CharField(verbose_name="Venue", max_length=250)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to="Venue Image/",
        verbose_name="Venue Image",
        validators=[validate_image],
    )
    city = models.ForeignKey(
        "Cities", default=1, on_delete=models.CASCADE, verbose_name="City"
    )
    date_added = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Date Added"
    )

    class Meta:
        verbose_name_plural = "Venues"

    def __str__(self):
        return self.venue


class Categories(models.Model):
    category = models.CharField(verbose_name="Category", max_length=150)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class Events(models.Model):
    organizer = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    eventName = models.CharField(verbose_name="Event Name", max_length=250)
    # eventDescription = RichTextUploadingField(
    #     config_name="portal_config", verbose_name="Event Description"
    # )
    eventDescription = models.TextField(verbose_name="Event Description")
    # eventCategory = models.
    payment = models.CharField(choices=PAID, verbose_name="Payment", max_length=50)

    eventCategories = MultiSelectField(
        choices=CATEGORIES,
        max_length=500,
        verbose_name="Event Category",
        blank=True,
        null=True,
    )

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
    eventLocation = models.CharField(
        max_length=150,
        verbose_name="Event Location",
        blank=True,
        null=True,
    )

    status = models.CharField(verbose_name="Status", default="Upcoming", max_length=250)
    eventType = models.CharField(
        choices=types, verbose_name="Event Type", max_length=250
    )
    venue = models.CharField(verbose_name="Venue", max_length=250)
    eventCity = models.ForeignKey(
        Cities,
        verbose_name="Event City",
        on_delete=models.SET_DEFAULT,
        default="Ethiopia",
    )
    eventCountry = models.CharField(
        verbose_name="Event Country", default="Ethiopia", max_length=250
    )
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")
    is_published = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.eventName

    # def get_absolute_url(self):
    #     erse("_detail", kwargs={"pk": self.pk})


class Images(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        reversed = fieldfile_obj.file.name[::-1]
        ext = reversed.split(".")[0][::-1]
        if not ext in settings.IMAGE_EXT:
            raise ValidationError(
                "File type not supported! Please upload only:  .jpg, .jpeg, .png format files."
            )
        megabyte_limit = 15.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    event = models.ForeignKey(Events, verbose_name="Event" ,on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(verbose_name="Image", upload_to="Event_Images/")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    # resizing the image, you can change parameters like size and quality.

    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 1125 or img.width > 1125:
            img.thumbnail((1125, 1125))
        img.save(self.image.path, quality=85, optimize=True)

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.event.eventName

from django.db import models

# Create your models here.

class Messages(models.Model):

    phoneNumber = models.CharField(max_length=15)   
    message = models.CharField(max_length=200)
    dateAdded = models.DateTimeField(auto_now_add=True)
    isSent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.phoneNumber 
    class Meta:
        verbose_name_plural = ("Messages")

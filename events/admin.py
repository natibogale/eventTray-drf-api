from django.contrib import admin

# Register your models here.
from .models import (Events,Venues)

admin.site.register(Events)
admin.site.register(Venues)

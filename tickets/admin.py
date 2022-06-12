from django.contrib import admin

# Register your models here.
from .models import (Tickets,TicketsBought)

admin.site.register(Tickets)
#register tickets bought model
admin.site.register(TicketsBought)
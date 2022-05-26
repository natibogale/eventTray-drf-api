from django.contrib import admin

# Register your models here.
from .models import (Events,Venues,Categories,Images,Cities)


class ImageAdmin(admin.StackedInline):
    model = Images

class EventAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = Events



admin.site.register(Events, EventAdmin)
admin.site.register(Venues)
admin.site.register(Images)
admin.site.register(Categories)
admin.site.register(Cities)


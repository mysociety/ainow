from django.contrib import admin
from conference import models

admin.site.register(models.Speaker)
admin.site.register(models.Schedule)
admin.site.register(models.Slot)
admin.site.register(models.Room)
admin.site.register(models.Presentation)

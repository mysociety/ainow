from django.contrib import admin
from conference import models


class SlotInline(admin.TabularInline):
    model = models.Slot
    extra = 1


admin.site.register(
    models.Schedule,
    prepopulated_fields={"slug": ("name",)},
    list_display=("name",),
    inlines = [SlotInline, ]
)

admin.site.register(models.Speaker)
admin.site.register(models.Slot)
admin.site.register(models.Room)
admin.site.register(models.Presentation)

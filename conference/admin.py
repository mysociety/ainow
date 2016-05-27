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

admin.site.register(models.Speaker, list_display=("name", "twitter_username"))
admin.site.register(models.Attendee, list_display=("name", "twitter_username"))
admin.site.register(
    models.Slot,
    list_display=("name", "kind", "start", "end", "room"),
    ordering=("start",)
)
admin.site.register(models.Room)
admin.site.register(
    models.Presentation,
    list_display=("title", "primary_speaker", "slot"),
    ordering=("slot__start",)
)

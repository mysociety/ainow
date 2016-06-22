from django.contrib import admin
from conference import models

from sorl.thumbnail.admin import AdminImageMixin


class SlotInline(admin.StackedInline):
    model = models.Slot
    extra = 1


admin.site.register(
    models.Schedule,
    prepopulated_fields={"slug": ("name",)},
    list_display=("name",),
    inlines = [SlotInline, ]
)


class SpeakerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Speaker, SpeakerAdmin)


class AttendeeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Attendee, AttendeeAdmin)


admin.site.register(
    models.Slot,
    list_display=("name", "kind", "start", "end", "room"),
    ordering=("start",)
)


admin.site.register(models.Room)


admin.site.register(
    models.Presentation,
    list_display=("title", "primary_speaker", "slot"),
    prepopulated_fields = {"slug": ("title",)},
    ordering=("slot__start",)
)

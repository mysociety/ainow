from django.contrib import admin
from conference import models

from sorl.thumbnail.admin import AdminImageMixin
from adminsortable2.admin import SortableAdminMixin


class SlotInline(admin.TabularInline):
    model = models.Slot
    extra = 1
    ordering = ['start']

    class Media:
        css = {
            'all': ('sass/admin_overrides.css',)
        }


admin.site.register(
    models.Schedule,
    prepopulated_fields={"slug": ("name",)},
    list_display=("name",),
    inlines = [SlotInline, ]
)


class SpeakerAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username", "title", "organisation")
    list_editable = ("twitter_username", "title", "organisation")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Speaker, SpeakerAdmin)


class OrganiserScheduleTypeInline(admin.TabularInline):
    model = models.Organiser.organiser_schedule_type.through


class OrganiserAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [OrganiserScheduleTypeInline,]

admin.site.register(
    models.OrganiserType,
)
admin.site.register(models.Organiser, OrganiserAdmin)


class AttendeeAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username", "title", "organisation")
    list_editable = ("twitter_username", "title", "organisation")
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

admin.site.register(
    models.LiveStream,
    list_display=("name", "youtube_link", "live"),
    list_editable=("youtube_link", "live"),
)


class StandingCommitteeAdmin(SortableAdminMixin, AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username", "title", "organisation")
    list_editable = ("twitter_username", "title", "organisation")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.StandingCommittee, StandingCommitteeAdmin)

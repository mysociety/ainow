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


class SpeakerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username", "title", "organisation")
    list_editable = ("twitter_username", "title", "organisation")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Speaker, SpeakerAdmin)


class OrganiserAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.OrganiserType)
admin.site.register(models.Organiser, OrganiserAdmin)


class AttendeeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("name", "twitter_username", "title", "organisation")
    list_editable = ("twitter_username", "title", "organisation")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Attendee, AttendeeAdmin)


class SessionsInline(admin.TabularInline):
    model = models.Session


admin.site.register(
    models.Slot,
    list_display=("start", "end"),
    ordering=("start",),
    inlines=[SessionsInline]
)


admin.site.register(models.Room)


class PresentationsInline(admin.TabularInline):
    model = models.Presentation

admin.site.register(
    models.Session,
    list_display=("name", "slot"),
    prepopulated_fields = {"slug": ("name",)},
    ordering=("slot__start",),
    inlines=[PresentationsInline]
)


admin.site.register(
    models.Presentation,
    list_display=("title", "session"),
    prepopulated_fields = {"slug": ("title",)},
    ordering=("session__slot__start",)
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

from django.contrib import admin
from themes.models import Theme

admin.site.register(
    Theme,
    prepopulated_fields={"slug": ("title",)},
    list_display=("name",)
)

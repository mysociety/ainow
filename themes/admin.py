from django.contrib import admin
from themes.models import Theme, Document

class DocumentInline(admin.StackedInline):
    model = Document
    extra = 1


admin.site.register(
    Theme,
    prepopulated_fields={"slug": ("title",)},
    list_display=("name",),
    inlines = [DocumentInline, ]
)

admin.site.register(Document)

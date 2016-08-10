from django.contrib import admin
from .models import Category, Document


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 1


admin.site.register(
    Category,
    list_display=("name",),
    inlines = [DocumentInline, ]
)

admin.site.register(Document)

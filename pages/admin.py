from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

from .models import Page


class SubPageInline(SortableInlineAdminMixin, admin.StackedInline):
	model = Page
	verbose_name_plural = 'sub-pages'
	verbose_name = 'sub-page'
	extra = 1


class PageAdmin(admin.ModelAdmin):
    inlines = (SubPageInline,)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Page, PageAdmin)
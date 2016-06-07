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

    def formfield_for_db_field(self, db_field, **kwargs):
	    if db_field.name == 'content':
	        kwargs['widget'] = AdminMarkItUpWidget()
	    return super(PageAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Page, PageAdmin)
from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

from .models import Page


class SubPageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Page
    verbose_name_plural = 'sub-pages'
    verbose_name = 'sub-page'
    extra = 1
    readonly_fields = ['schedules']


class PageAdmin(admin.ModelAdmin):
    inlines = (SubPageInline,)
    prepopulated_fields = {"slug": ("title",)}

    def formfield_for_db_field(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = AdminMarkItUpWidget()
        return super(PageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # You can't set the schedules if this is a sub-page
        # (You have to set it on the parent page)
        readonly_fields = super(PageAdmin, self).get_readonly_fields(request, obj)
        if obj and obj.parent_page:
            return readonly_fields + ('schedules',)
        return readonly_fields



admin.site.register(Page, PageAdmin)

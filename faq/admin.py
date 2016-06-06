from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

from faq.models import FAQPage, FAQQuestion, FAQQuestionPage


class FAQQuestionPageInline(SortableInlineAdminMixin, admin.StackedInline):
	model = FAQQuestion.pages.through
	verbose_name_plural = 'questions'
	verbose_name = 'question'
	extra = 1


class FAQPageAdmin(admin.ModelAdmin):
    inlines = (FAQQuestionPageInline,)
    prepopulated_fields = {"slug": ("title",)}


# This is identical to FAQQuestionPageInline in a practical
# sense, but it sets up a bunch of different names/labels to make
# more sense to the user.
class FAQPageQuestionInline(SortableInlineAdminMixin, admin.StackedInline):
	model = FAQQuestion.pages.through
	verbose_name_plural = 'pages'
	verbose_name = 'page'
	extra = 1


class FAQQuestionAdmin(admin.ModelAdmin):
	inlines = (FAQPageQuestionInline,)
	prepopulated_fields = {"slug": ("question",)}


admin.site.register(FAQPage, FAQPageAdmin)
admin.site.register(FAQQuestion, FAQQuestionAdmin)

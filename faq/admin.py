from django.contrib import admin
from faq.models import FAQPage, FAQQuestion


admin.site.register(FAQPage, prepopulated_fields={"slug": ("title",)},)
admin.site.register(FAQQuestion, prepopulated_fields={"slug": ("question",)},)

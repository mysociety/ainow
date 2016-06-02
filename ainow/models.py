from django.db import models


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    slug = models.SlugField(help_text="Used to make a nice url for the page that displays this.")

    class Meta:
        abstract = True

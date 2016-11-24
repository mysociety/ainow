from django.conf import settings

from markdown import markdown
from bleach import clean


def bleached_markdown(input):
    return clean(
        markdown(input),
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
        protocols=settings.BLEACH_ALLOWED_PROTOCOLS
    )

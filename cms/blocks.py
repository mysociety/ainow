from wagtail.wagtailcore import blocks
from django.utils import html
from django.conf import settings
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from conference.models import Schedule

class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = 'cms/blocks/heading.html',
        icon = 'title'
        classname = 'title'

class TextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'cms/blocks/text.html'

class MissionBlock(blocks.RichTextBlock):
    class Meta:
        template='cms/blocks/mission.html',
        icon='edit'

class DividerBlock(blocks.StaticBlock):
    class Meta:
        admin_text=html.mark_safe("<hr>")
        template='cms/blocks/divider.html'
        icon='horizontalrule'

class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock()
    class Meta:
        template='cms/blocks/link.html'

class FeaturedLinkBlock(blocks.StructBlock):
    title = HeadingBlock()
    subtitle = blocks.CharBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    thumbnail = ImageChooserBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)
    class Meta:
        template='cms/blocks/featured_link.html'

class FeatureBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    text =  blocks.RichTextBlock()
    links = blocks.ListBlock(LinkBlock())
    class Meta:
        icon='doc-full'

class ColumnBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock()
    class Meta:
        icon='doc-full'

class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    position = blocks.CharBlock()
    organisation = blocks.CharBlock()
    image = ImageChooserBlock()
    class Meta:
        icon='user'

class YouTubeBlock(EmbedBlock):
    class Meta:
        icon='media'
        template='cms/blocks/youtube.html'

class EventBlock(blocks.StructBlock):
    name = HeadingBlock()
    start = blocks.DateTimeBlock(label="Start date/time")
    end = blocks.DateTimeBlock(label="End date/time")
    location = TextBlock()
    link = blocks.URLBlock(required=False)
    schedule = blocks.ChoiceBlock(
        required=False,
        choices=tuple([(element.slug, element.name) for element in Schedule.objects.all()])
    )
    class Meta:
        icon='date'

class MailChimpBlock(blocks.StructBlock):
    title = HeadingBlock()
    intro = TextBlock(required=False)
    list_id = blocks.CharBlock(required=False,help_text='The list ID for your Mailchimp link (default is '+ settings.MAILCHIMP_DEFAULT_LIST_ID +')'  )
    class Meta:
        icon='mail'
        template='cms/blocks/mailchimp.html'

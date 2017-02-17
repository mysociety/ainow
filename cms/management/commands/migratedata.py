from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page as WagtailPage
from pages.models import Page
from cms.models import SimplePage, HomePage

class Command(BaseCommand):
    help = 'Migrates pages to Wagtail CMS'

    def handle(self, *args, **options):
        root_page = HomePage.objects.all()[0]

        for page in Page.objects.all():
            p = SimplePage(
                title=page.title,
                name=page.name,
                slug=page.slug,
                body=page.content
            )
            root_page.add_child(instance=p)
            page.delete()
            self.stdout.write(self.style.SUCCESS('Page \'%s\' migrated' % page.title))

        self.stdout.write(self.style.SUCCESS('All pages migrated successfully!'))

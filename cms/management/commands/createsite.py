from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Site
from cms.models import HomePage

class Command(BaseCommand):
    help = 'Sets up a brand new Wagtail CMS site'

    def handle(self, *args, **options):
        root_page = Page.get_first_root_node()
        site_name = 'Artificial Intelligence Now' # This could probably be set up by args
        # Delete any existing sites
        Site.objects.all().delete()

        # Create a root page
        page = HomePage(
            title=site_name,
            path='0001',
            depth=2
        )
        root_page.add_child(instance=page)

        # Create a new sites
        site = Site(
            hostname='localhost',
            port='8000',
            is_default_site=True,
            root_page_id=page.id,
            site_name=site_name
        )
        site.save()

        # Delete the default Wagtail Homepage
        Page.objects.filter(title='Welcome to your new Wagtail site!').delete()

        self.stdout.write(self.style.SUCCESS('Site %s created!' % site_name))

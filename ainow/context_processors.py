from django.conf import settings

from conference.models import Schedule


def add_settings(request):
    """Add some selected settings values to the context"""
    return {
        'settings': {
            'GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
            'DEBUG': settings.DEBUG,
        },
        # For some reason this doesn't work if we put it inside settings
        'CONTACT_EMAIL': settings.CONTACT_EMAIL
    }


def add_schedule(request):
    """ do not hide private schedules from staff members to make updating
        those easier"""
    if (request.user.is_staff):
        context = {
            'schedules': Schedule.objects.all().order_by('-name')
        }
    else:
        context = {
            'schedules': Schedule.objects.exclude(private=True).order_by('-name')
        }
    # We can't modify the account views to set this directly, so we set it here instead
    if request.resolver_match.url_name.startswith("account"):
        context.update({'schedule': Schedule.objects.get(slug='2016')})

    return context

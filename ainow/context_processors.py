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
    """Force the schedule variable to a set value for certain requests"""
    # We can't modify the account views to set this directly, so we set it here instead
    context = {
        'schedules': Schedule.objects.all()
    }
    if request.resolver_match.url_name.startswith("account"):
        context.update({'schedule': Schedule.objects.get(slug='2016')})

    return context

from django.conf import settings


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

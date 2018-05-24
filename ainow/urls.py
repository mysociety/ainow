"""ainow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .views import (
    HomeView,
    SignupView,
    LoginView,
    ConfirmEmailView,
    PrivacyView,
)
from faq.views import FAQPageView

admin.autodiscover()

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    url(r"^schedule/(?P<schedule_slug>[-\w]+)/faq/(?P<slug>[-\w]+)$", FAQPageView.as_view(), name="faq"),

    url(r'^', include('conference.urls')),
    url(r'^', include('resources.urls')),

    # Override the login and signup views from the account app, so we can use
    # our versions which use an email address instead of a username.
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", LoginView.as_view(), name="account_login"),
    # Override the confirm_email view from the account app, so we can sign
    # people in immediately after they confirm.
    url(r"^account/confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^account/", include("account.urls")),

    url(r'^privacy/$', PrivacyView.as_view(), name='privacy'),

    url(r'^admin/', admin.site.urls),
    url(r'^markitup/', include('markitup.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

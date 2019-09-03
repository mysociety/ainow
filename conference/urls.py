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
from django.conf.urls import url

from .views import (
    ScheduleView,
    Schedule2017SummaryView,
    ScheduleTaipeiSummaryView,
    Schedule2018SummaryView,
    Schedule2018SpeakerListView,
    Schedule2019SummaryView,
    Schedule2019SpeakerListView,
    Schedule2020SummaryView,
    Schedule2020SpeakerListView,
    SponsorshipView,
    LocalView,
    Local2018View,
    Local2019View,
    SpeakerListView,
    SpeakerView,
    OrganiserTypeListView,
    PresentationListView,
    PresentationView,
    AttendeeListView,
    AttendeeView,
    AttendeeCreateUpdateView,
    StandingCommitteeListView,
    delete_photo
)

from django.views.generic import RedirectView

from pages.views import PageView

urlpatterns = [

    # Redirects from legacy URLs

    url(r'^schedule/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='schedule', permanent=True)),

    url(r'^schedule/(?P<schedule_slug>[-\w]+)/presentations$', RedirectView.as_view(pattern_name='presentations', permanent=True)),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/presentation/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='presentation', permanent=True)),

    url(r'^schedule/(?P<schedule_slug>[-\w]+)/speakers$', RedirectView.as_view(pattern_name='speakers', permanent=True)),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/speaker/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='speaker', permanent=True)),

    # This is an Americization of "organisers" within the context of the conference.
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/organizers$', RedirectView.as_view(pattern_name='organisers', permanent=True)),

    url(r'^schedule/(?P<schedule_slug>[-\w]+)/attendees$', RedirectView.as_view(pattern_name='attendees', permanent=True)),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/attendee/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='attendee', permanent=True)),

    url(r'^schedule/(?P<schedule_slug>[-\w]+)/page/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='staticpage', permanent=True)),

    # TICTeC Local

    url(r'^local$', LocalView.as_view(), name='local'),
    url(r'^local/2018$', Local2018View.as_view(), name='local-2018'),
    url(r'^local/2019$', Local2019View.as_view(), name='local-2019'),

    # URLs for profile management

    url(r"^profile/$", AttendeeCreateUpdateView.as_view(), name="profile"),
    url(r"^profile/delete-photo$", delete_photo, name="profile_delete_photo"),

    # New-style 'schedule-free' URLs

    url(r'^(?P<slug>[-\w]+)/schedule$', ScheduleView.as_view(), name='schedule'),

    url(r'^(?P<schedule_slug>[-\w]+)/presentations$', PresentationListView.as_view(), name='presentations'),
    url(r'^(?P<schedule_slug>[-\w]+)/presentation/(?P<slug>[-\w]+)$', PresentationView.as_view(), name='presentation'),

    url(r'^2018/speakers$', Schedule2018SpeakerListView.as_view(), {'schedule_slug': '2018'}, name='2018speakers'),
    url(r'^2019/speakers$', Schedule2019SpeakerListView.as_view(), {'schedule_slug': '2019'}, name='2019speakers'),
    url(r'^2020/speakers$', Schedule2020SpeakerListView.as_view(), {'schedule_slug': '2020'}, name='2020speakers'),

    url(r'^(?P<schedule_slug>[-\w]+)/speakers$', SpeakerListView.as_view(), name='speakers'),
    url(r'^(?P<schedule_slug>[-\w]+)/speaker/(?P<slug>[-\w]+)$', SpeakerView.as_view(), name='speaker'),

    url(r'^(?P<schedule_slug>[-\w]+)/organisers$', OrganiserTypeListView.as_view(), name='organisers'),

    url(r'^(?P<schedule_slug>[-\w]+)/attendees$', AttendeeListView.as_view(), name='attendees'),
    url(r'^(?P<schedule_slug>[-\w]+)/attendee/(?P<slug>[-\w]+)$', AttendeeView.as_view(), name='attendee'),

    url(r'^2017$', Schedule2017SummaryView.as_view(), name='schedule2017summary'),

    url(r'^taipei$', ScheduleTaipeiSummaryView.as_view(), name='scheduletaipeisummary'),

    url(r'^2018$', Schedule2018SummaryView.as_view(), name='schedule2018summary'),

    url(r'^2019$', Schedule2019SummaryView.as_view(), name='schedule2019summary'),

    url(r'^2020$', Schedule2020SummaryView.as_view(), name='schedule2020summary'),

    # This must come after all other URLs, as a catch-all
    url(r'^(?P<schedule_slug>[-\w]+)/(?P<slug>[-\w]+)$', PageView.as_view(), name='staticpage'),

    url(r'^sponsorship$', SponsorshipView.as_view(), name='sponsorship'),

]

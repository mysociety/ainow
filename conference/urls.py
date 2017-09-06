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
    Schedule2018SummaryView,
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

    # URLs for profile management

    url(r"^profile/$", AttendeeCreateUpdateView.as_view(), name="profile"),
    url(r"^profile/delete-photo$", delete_photo, name="profile_delete_photo"),

    # New-style 'schedule-free' URLs

    url(r'^(?P<slug>[-\w]+)/schedule$', ScheduleView.as_view(), name='schedule'),

    url(r'^(?P<schedule_slug>[-\w]+)/presentations$', PresentationListView.as_view(), name='presentations'),
    url(r'^(?P<schedule_slug>[-\w]+)/presentation/(?P<slug>[-\w]+)$', PresentationView.as_view(), name='presentation'),

    url(r'^(?P<schedule_slug>[-\w]+)/speakers$', SpeakerListView.as_view(), name='speakers'),
    url(r'^(?P<schedule_slug>[-\w]+)/speaker/(?P<slug>[-\w]+)$', SpeakerView.as_view(), name='speaker'),

    url(r'^(?P<schedule_slug>[-\w]+)/organisers$', OrganiserTypeListView.as_view(), name='organisers'),

    url(r'^(?P<schedule_slug>[-\w]+)/attendees$', AttendeeListView.as_view(), name='attendees'),
    url(r'^(?P<schedule_slug>[-\w]+)/attendee/(?P<slug>[-\w]+)$', AttendeeView.as_view(), name='attendee'),

    url(r'^2017$', Schedule2017SummaryView.as_view(), name='schedule2017summary'),
    url(r'^2018$', Schedule2018SummaryView.as_view(), name='schedule2018summary'),
]

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

from .views import (
    ScheduleView,
    SpeakerListView,
    WorkshopSpeakerListView,
    PresentationView,
    AttendeeListView,
    SpeakerCreateUpdateView
)

urlpatterns = [
    url(r'^schedule/(?P<slug>[-\w]+)$', ScheduleView.as_view(), name='schedule'),
    url(r'^presentation/(?P<slug>[-\w]+)$', PresentationView.as_view(), name='presentation'),
    url(r'^speakers$', SpeakerListView.as_view(), name='speakers'),
    
    # Workshop urls, mostly a repetition of the other views, but showing
    # different content for the private section of the site
    url(r'^workshop/attendees$', AttendeeListView.as_view(), name='workshop_attendees'),
    url(r'^workshop/speakers$', WorkshopSpeakerListView.as_view(), name='workshop_speakers'),

    url(r"^profile/$", SpeakerCreateUpdateView.as_view(), name="profile"),
]

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
    SpeakerListView,
    SpeakerView,
    PresentationView,
    AttendeeListView,
    AttendeeView,
    AttendeeCreateUpdateView,
    delete_photo
)

urlpatterns = [
    url(r'^schedule/(?P<slug>[-\w]+)$', ScheduleView.as_view(), name='schedule'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/presentation/(?P<slug>[-\w]+)$', PresentationView.as_view(), name='presentation'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/speakers$', SpeakerListView.as_view(), name='speakers'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/speaker/(?P<slug>[-\w]+)$', SpeakerView.as_view(), name='speaker'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/attendees$', AttendeeListView.as_view(), name='attendees'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/attendee/(?P<slug>[-\w]+)$', AttendeeView.as_view(), name='attendee'),
    url(r"^profile/$", AttendeeCreateUpdateView.as_view(), name="profile"),
    url(r"^profile/delete-photo$", delete_photo, name="profile_delete_photo"),
]

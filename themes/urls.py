from django.conf import settings
from django.conf.urls import url, include

from .views import (
    ThemeListView,
    ThemeView
)

urlpatterns = [
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/themes$', ThemeListView.as_view(), name='themes'),
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/theme/(?P<slug>[-\w]+)$', ThemeView.as_view(), name='theme'),
]

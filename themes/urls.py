from django.conf.urls import url

from .views import ThemeListView

urlpatterns = [
    url(r'^schedule/(?P<schedule_slug>[-\w]+)/themes$', ThemeListView.as_view(), name='themes'),
]

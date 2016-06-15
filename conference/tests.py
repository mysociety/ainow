import os
import tempfile
import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings

from .models import Attendee, Schedule


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(),
                                STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage')
class AttendeeProfileTest(TestCase):
    def setUp(self):
        self.schedule = Schedule.objects.create(slug='workshop', name='Workshop', private=True)
        self.user = User.objects.create_user('test_attendee', 'attendee@example.com', 'password')
        self.client.login(username='test_attendee', password='password')
        self.filename = os.path.join(settings.PROJECT_ROOT, 'conference', 'fixtures', 'attendee.jpg')
        self.filename2 = os.path.join(settings.PROJECT_ROOT, 'conference', 'fixtures', 'attendee2.jpg')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_creating_new_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        with open(self.filename) as attendee_photo:
            response = self.client.post(
                reverse('profile'),
                {
                    'name': 'Test Attendee',
                    'photo': attendee_photo,
                    'twitter_username': '@test',  # The @ should be stripped
                    'organisation': 'test org'
                }
            )
            self.assertRedirects(response, reverse('profile'))
        profile = Attendee.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Attendee')
        self.assertNotEqual(profile.photo, None)
        self.assertEqual(profile.twitter_username, 'test')
        self.assertEqual(profile.organisation, 'test org')

    def test_updating_profile(self):
        with open(self.filename) as attendee_photo:
            wrapped_attendee_photo = File(attendee_photo)
            profile = Attendee.objects.create(
                user=self.user,
                name='Test Attendee',
                photo=wrapped_attendee_photo,
                twitter_username='test',
                organisation='test org'
            )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        # So that we can check it's changed later
        original_photo_path = profile.photo.path

        with open(self.filename2) as attendee_photo2:
            response = self.client.post(
                reverse('profile'),
                {
                    'name': 'Test Attendee Updated',
                    'photo': attendee_photo2,
                    'twitter_username': '@test_updated',  # The @ should be stripped
                    'organisation': 'test org updated'
                }
            )
        self.assertRedirects(response, reverse('profile'))
        profile = Attendee.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Attendee Updated')
        self.assertNotEqual(profile.photo.path, original_photo_path)
        self.assertEqual(profile.twitter_username, 'test_updated')
        self.assertEqual(profile.organisation, 'test org updated')

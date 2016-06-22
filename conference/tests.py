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


@override_settings(
    MEDIA_ROOT=tempfile.mkdtemp(),
    STATICFILES_STORAGE='pipeline.storage.NonPackagingPipelineStorage'
)
class AttendeeProfileTest(TestCase):
    def setUp(self):
        self.schedule = Schedule.objects.create(slug='workshop', name='Workshop', private=True)
        self.user = User.objects.create_user('test_attendee', 'attendee@example.com', 'password')
        self.client.login(username='test_attendee', password='password')
        fixture_dir = os.path.join(settings.PROJECT_ROOT, 'conference', 'fixtures')
        self.filename = os.path.join(fixture_dir, 'attendee.jpg')
        self.filename2 = os.path.join(fixture_dir, 'attendee2.jpg')
        self.filename_too_small = os.path.join(fixture_dir, 'attendee_too_small.jpg')

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
                    'organisation': 'test org',
                    'title': 'test title',
                    'biography': 'Test biography'
                }
            )
            self.assertRedirects(response, reverse('profile'))
        profile = Attendee.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Attendee')
        self.assertNotEqual(profile.photo, None)
        self.assertEqual(profile.twitter_username, 'test')
        self.assertEqual(profile.organisation, 'test org')
        self.assertEqual(profile.title, 'test title',)
        self.assertEqual(profile.biography, 'Test biography')

    def test_updating_profile(self):
        with open(self.filename) as attendee_photo:
            wrapped_attendee_photo = File(attendee_photo)
            profile = Attendee.objects.create(
                user=self.user,
                name='Test Attendee',
                photo=wrapped_attendee_photo,
                twitter_username='test',
                title='test title',
                organisation='test org',
                biography='test biography'
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
                    'organisation': 'test org updated',
                    'title': 'test title updated',
                    'biography': 'Test biography updated'
                }
            )
        self.assertRedirects(response, reverse('profile'))
        profile = Attendee.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Attendee Updated')
        self.assertNotEqual(profile.photo.path, original_photo_path)
        self.assertEqual(profile.twitter_username, 'test_updated')
        self.assertEqual(profile.organisation, 'test org updated')
        self.assertEqual(profile.title, 'test title updated',)
        self.assertEqual(profile.biography, 'Test biography updated')

    def test_photo_size_validation(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        with open(self.filename_too_small) as attendee_photo:
            response = self.client.post(
                reverse('profile'),
                {
                    'name': 'Test Attendee',
                    'photo': attendee_photo,
                }
            )
            self.assertFormError(
                response,
                'form',
                'photo',
                'Do you have a bigger picture? Photos must be at least 500px by 500px.'
            )

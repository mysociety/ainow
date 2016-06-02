import os
import tempfile
import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings

from .models import Speaker


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SpeakerProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_speaker', 'speaker@example.com', 'password')
        self.client.login(username='test_speaker', password='password')
        self.filename = os.path.join(settings.PROJECT_ROOT, 'conference', 'fixtures', 'speaker.jpg')
        self.filename2 = os.path.join(settings.PROJECT_ROOT, 'conference', 'fixtures', 'speaker2.jpg')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_creating_new_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        with open(self.filename) as speaker_photo:
            response = self.client.post(
                reverse('profile'),
                {
                    'name': 'Test Speaker',
                    'biography': 'This is a **test** _biography_',
                    'photo': speaker_photo,
                    'twitter_username': 'test',
                    'website': 'http://www.example.com',
                    'facebook': 'http://facebook.com/test_speaker'
                }
            )
            self.assertRedirects(response, reverse('profile'))
        profile = Speaker.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Speaker')
        self.assertEqual(profile.biography.raw, 'This is a **test** _biography_')
        self.assertNotEqual(profile.photo, None)
        self.assertEqual(profile.twitter_username, 'test')
        self.assertEqual(profile.website, 'http://www.example.com')
        self.assertEqual(profile.facebook, 'http://facebook.com/test_speaker')

    def test_updating_profile(self):
        with open(self.filename) as speaker_photo:
            wrapped_speaker_photo = File(speaker_photo)
            profile = Speaker.objects.create(
                user=self.user,
                name='Test Speaker',
                biography='This is a **test** _biography_',
                photo=wrapped_speaker_photo,
                twitter_username='test',
                website='http://www.example.com',
                facebook='http://facebook.com/test_speaker'
            )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        # So that we can check it's changed later
        original_photo_path = profile.photo.path

        with open(self.filename2) as speaker_photo2:
            response = self.client.post(
                reverse('profile'),
                {
                    'name': 'Test Speaker Updated',
                    'biography': 'This is a **test** _biography_ updated',
                    'photo': speaker_photo2,
                    'twitter_username': 'test_updated',
                    'website': 'http://www.example.com/updated',
                    'facebook': 'http://facebook.com/test_speaker_updated'
                }
            )
        self.assertRedirects(response, reverse('profile'))
        profile = Speaker.objects.get(user=self.user)
        self.assertEqual(profile.name, 'Test Speaker Updated')
        self.assertEqual(profile.biography.raw, 'This is a **test** _biography_ updated')
        self.assertNotEqual(profile.photo.path, original_photo_path)
        self.assertEqual(profile.twitter_username, 'test_updated')
        self.assertEqual(profile.website, 'http://www.example.com/updated')
        self.assertEqual(profile.facebook, 'http://facebook.com/test_speaker_updated')

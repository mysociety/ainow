from django.test import TestCase
from .models import HomePage, SimplePage

class HomePageTest(TestCase):

    def test_home_page(self):
        h = HomePage(
            title='Welcome to the homepage',
            body='<p>Some HTML goes here, blah, blah',
            
        )

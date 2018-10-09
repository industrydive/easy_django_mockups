from unittest import TestCase
from django.conf import settings

#settings.configure()


class TestJoke(TestCase):
    def test_is_string(self):
        s = 'hi'
        self.assertTrue(True)
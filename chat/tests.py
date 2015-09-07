from django.test import TestCase
from django.test.client import Client


# Create your tests here.
class ChatTests(TestCase):
    client_class = Client

    def test(self):
        self.assertEqual(1 + 1, 2)

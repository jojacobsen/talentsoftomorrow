
import unittest
from unittest import mock
from django.contrib.auth.models import User
from .utils import create_username, lab_key_generator


class TestUtils(unittest.TestCase):
    def test_create_username(self):
        last_name = 'Doe'
        first_name = 'John'
        username = create_username(last_name, first_name)

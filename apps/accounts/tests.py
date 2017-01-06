from unittest import mock
import unittest


class TestUtils(unittest.TestCase):
    @mock.patch('apps.accounts.utils.random')
    def test_create_username(self, mock_random):
        from apps.accounts.utils import create_username
        last_name = 'Doe'
        first_name = 'John'
        mock_random.randrange.return_value = 94156
        username = create_username(last_name, first_name)
        self.assertEquals('jdoe94156', username)

    @mock.patch('apps.accounts.utils.random')
    def test_lab_key_generator(self, mock_random):
        from apps.accounts.utils import lab_key_generator
        mock_random.choice.return_value = 'a'
        lab_key = lab_key_generator()
        self.assertEquals('aaaaa', lab_key)


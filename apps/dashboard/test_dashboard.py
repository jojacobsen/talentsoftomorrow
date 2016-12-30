import pytest
import json
import unittest
from django.test import Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from dashboard import views


@pytest.mark.django_db
class IndexViewTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_serve(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class EndpointViewTest(APITestCase):
    """
    Test the Endpoint functions.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user, self.created = User.objects.get_or_create(username='testuser', email='testuser@talentstomorrow.com')
        if self.created:
            self.user.set_password('password')
        self.token, self.created = Token.objects.get_or_create(user=self.user)
        if self.created:
            self.token.save()
'''
    def test_post_data(self):
        view = views.TestAPI.as_view()
        request = self.factory.post('/push', json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        #self.assertEqual(response.status_code, 201)

    def test_post_incorrect_data(self):
        data[0].pop("startPos", None)
        view = views.TestAPI.as_view()
        request = self.factory.post('/push', json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        #self.assertEqual(response.status_code, 400)
'''
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


class TestSerializers(unittest.TestCase):
    @mock.patch('apps.accounts.serializers.Player')
    @mock.patch('apps.accounts.serializers.User')
    @mock.patch('apps.accounts.serializers.lab_key_generator')
    @mock.patch('apps.accounts.serializers.Group')
    @mock.patch('apps.accounts.serializers.create_username')
    def test_new_player_serializer_create(self, mock_create_username, mock_group, mock_lab_key_generator,
                                          mock_user, mock_player):
        from apps.accounts.serializers import NewPlayerSerializer
        username = 'jdoe94156'
        lab_key = 'aaaaa'
        request = mock.MagicMock()
        request.user.groups.values_list.return_value = 'Club'
        new_player = NewPlayerSerializer(context={'request': request})
        validated_data = mock.MagicMock()
        mock_group.objects.get.return_value = mock.MagicMock
        mock_user.objects.create_user.return_value = mock.MagicMock(username=username)
        mock_create_username.return_value = username
        mock_lab_key_generator.return_value = lab_key
        mock_player.objects.create.return_value = mock.MagicMock()
        player = new_player.create(validated_data)
        self.assertEquals(player, mock_player.objects.create.return_value)


class TestViews(unittest.TestCase):
    @mock.patch('apps.accounts.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.accounts.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)


    @mock.patch('apps.accounts.views.JSONResponse')
    @mock.patch('apps.accounts.views.JSONParser')
    @mock.patch('apps.accounts.views.NewPlayerSerializer')
    def test_playercreateview(self, mock_newplayerserializer, mock_jsonparser, mock_jsonrsponse):
        from apps.accounts.views import PlayerCreateView
        player = PlayerCreateView()
        json_response = mock.MagicMock()
        mock_jsonrsponse.return_value = json_response
        mock_newplayerserializer.return_value = mock.MagicMock()
        data = mock.MagicMock
        mock_jsonparser.return_value.parse.return_value = data
        request = mock.MagicMock()
        response = player.create(request, None)
        self.assertEquals(response, json_response)

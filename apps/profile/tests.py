from unittest import mock
import unittest


class TestViews(unittest.TestCase):
    @mock.patch('apps.profile.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.profile.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)

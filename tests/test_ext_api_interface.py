import sys
sys.path.append('../')
from library.library import Library
from library.patron import Patron
from unittest.mock import Mock, patch
import unittest
import requests
from requests import Response
from library.library_db_interface import Library_DB
from library.ext_api_interface import Books_API


class TestAPI(unittest.TestCase):

    def mock_request(self, status=200, json_data="You expected a json, but it was me! Dio!",  content="http://openlibrary.org/search.json", raise_for_status=None):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = Mock(return_value=json_data)
        return mock_resp

    @patch('requests.get')
    def test_make_request(self, mock_get):
        mock_resp = self.mock_request()
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.make_request("http://openlibrary.org/search.json")
        self.assertEqual("You expected a json, but it was me! Dio!", actual)

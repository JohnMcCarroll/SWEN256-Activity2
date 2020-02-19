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

    def mock_request(self, status=200, json_data={'docs': ["1", "2"]},  content="http://openlibrary.org/search.json", raise_for_status=None, error=None):
        mock_resp = Mock()

        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = Mock(return_value=json_data)
        else:
            mock_resp.json.return_value = None

        return mock_resp

    @patch('requests.get')
    def test_make_request(self, mock_get):
        mock_resp = self.mock_request()
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.make_request("http://openlibrary.org/search.json")
        self.assertEqual({'docs': ["1", "2"]}, actual)
        mock_resp = self.mock_request(status=500)
        mock_get.return_value = mock_resp
        actual = api.make_request("http://openlibrary.org/search.json")
        self.assertEqual(None,actual)

    @patch('requests.get')
    def test_make_request_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()
        mock_resp = self.mock_request(error=ConnectionError())
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.make_request("http://openlibrary.org/search.json")
        self.assertEqual(None, actual)

    @patch('requests.get')
    def test_is_book_available(self, mock_get):
        mock_resp = self.mock_request()
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.is_book_available("book")
        self.assertTrue(actual)

    @patch("requests.get")
    def test_is_book_available_false(self, mock_get):
        mock_resp = self.mock_request(json_data=None)
        mock_resp.json.return_value = None
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.is_book_available("book")
        self.assertFalse(actual)

    @patch("requests.get")
    def test_book_by_author(self, mock_get):
        mock_resp = self.mock_request(json_data={'docs': [{"title_suggest": "1984"}]})
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.books_by_author("author")
        self.assertEqual(["1984"], actual)

    @patch("requests.get")
    def test_book_by_author_fail(self, mock_get):
        mock_resp = self.mock_request(json_data=None)
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.books_by_author("author")
        self.assertEqual([], actual)

    @patch("requests.get")
    def test_get_book_info(self, mock_get):
        mock_resp = self.mock_request(json_data={'docs': [{"title": "1984", "publish_year": "Orwell", "publisher": "penguin", "language": "english"}]})
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.get_book_info("book")
        self.assertEqual([{"title": "1984", "publish_year": "Orwell", "publisher": "penguin", "language": "english"}], actual)

    @patch("requests.get")
    def test_get_book_info_fail(self, mock_get):
        mock_resp = self.mock_request(json_data=None)
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.get_book_info("book")
        self.assertEqual([], actual)

    @patch("requests.get")
    def test_get_ebooks(self, mock_get):
        mock_resp = self.mock_request(json_data={'docs': [{"title": "1984", "ebook_count_i": 2}]})
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.get_ebooks("book")
        self.assertEqual([{"title": "1984", "title": "1984", "ebook_count": 2}], actual)

    @patch("requests.get")
    def test_get_ebooks_fail(self, mock_get):
        mock_resp = self.mock_request(json_data=None)
        mock_get.return_value = mock_resp
        api = Books_API()
        actual = api.get_ebooks("book")
        self.assertEqual([], actual)

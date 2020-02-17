import sys
sys.path.append('../')
from library.library import Library
from library.patron import Patron
from unittest.mock import Mock, patch
import unittest
from library.library_db_interface import Library_DB
from library.ext_api_interface import Books_API


class TestLibrary(unittest.TestCase):
    @patch('library.ext_api_interface.Books_API')
    @patch('library.library_db_interface.Library_DB')
    def setUp(self, mockBooks_API, mockLibrary_DB):
        self.library = Library()
        self.patron = Patron("bob","bobson",41,1)
        self.library.api = mockBooks_API
        self.library.db = mockLibrary_DB
        mockBooks_API.get_ebooks.return_value = [{'title': 'The Count of Monte Cristo', "ebook_count" : 1},
                                                 {'title': 'A Tale of Two Cities', "ebook_count": 1},
                                                 {'title': '1984', "ebook_count": 1},
                                                 {'title': 'Slaughterhouse 5', "ebook_count": 1},
                                                 {'title': 'Breakfast of Champions', "ebook_count": 1}]
        mockBooks_API.books_by_author.return_value = ['Slaughterhouse 5', 'Breakfast of Champions']
        mockBooks_API.get_book_info.return_value = [{'title': 'The Count of Monte Cristo', "ebook_count": 1,
                                                     'publisher': 'Penguin', 'publish_year': '1844', 'language':
                                                         "french"}]
        mockLibrary_DB.patrons = [self.patron]
        mockLibrary_DB.update_patron = self.mock_update_patron
        mockLibrary_DB.insert_patron.return_value = 1
        mockLibrary_DB.retrieve_patron = self.mock_retrieve_patron

    def mock_update_patron(self,patron):
        self.library.db.patrons[0] = patron

    def mock_retrieve_patron(self, patron):
        if patron == 1:
            return self.library.db.patrons[0]
        else:
            return None

    def test_is_ebook(self):
        library = self.library
        self.assertFalse(library.is_ebook('title'))
        self.assertTrue(library.is_ebook("1984"))

    def test_get_ebooks_count(self):
        library = self.library
        self.assertEqual(library.get_ebooks_count('title'), 5)

    def test_is_book_by_author(self):
        library = self.library
        self.assertTrue(library.is_book_by_author("Kurt Vonnegut", 'Slaughterhouse 5'))
        self.assertFalse(library.is_book_by_author("Kurt Vonnegut", "1984"))

    def test_get_languages_for_book(self):
        library = self.library
        result = set('french')
        self.assertEqual(library.get_languages_for_book('The Count of Monte Cristo'), result)

    def test_register_patron(self):
        library = self.library
        self.assertEqual(library.register_patron("bob","bobson",41,1), 1)

    def test_is_patron_registered(self):
        library = self.library
        patron = self.patron
        p2 = Patron("bob","bobson",41,2)
        self.assertTrue(library.is_patron_registered(patron))
        self.assertFalse(library.is_patron_registered(p2))

    def test_borrow_book(self):
        library = self.library
        patron = self.patron
        library.borrow_book("1984", patron)
        self.assertEqual(self.library.db.retrieve_patron(1).get_borrowed_books(), ["1984"])

    def test_return_borrowed_book(self):
        library = self.library
        patron = self.patron
        library.borrow_book("1984", patron)
        library.return_borrowed_book("1984", patron)
        self.assertEqual(self.library.db.retrieve_patron(1).get_borrowed_books(),[])

    def test_is_book_borrowed(self):
        library = self.library
        patron = self.patron
        library.borrow_book("1984", patron)
        self.assertTrue(self.library.is_book_borrowed("1984", patron))

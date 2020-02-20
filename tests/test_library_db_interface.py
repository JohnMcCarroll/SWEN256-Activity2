import sys
sys.path.append('../')
from library.library_db_interface import Library_DB
from unittest.mock import Mock
import unittest
from library.patron import Patron

class TestDB(unittest.TestCase):

    def setUp(self):
        self.CuT = Library_DB()
        self.CuT.close_db()
        self.CuT.db = Mock()
        self.patron1 = Patron("Reggie", "Miller", 49, "987654321")
        self.patron2 = Patron("Todd", "Dodd", 20, "12345")
        self.patron1.add_borrowed_book("Old Man and the Sea")

    def test_insert_patron_not_Patron(self):
        self.assertIsNone(self.CuT.insert_patron(None))

    def test_insert_patron_already_inserted(self):
        self.CuT.retrieve_patron = Mock()
        self.CuT.retrieve_patron.return_value = self.patron2
        self.assertIsNone(self.CuT.insert_patron(self.patron2))

    def test_insert_patron_success(self):
        self.CuT.retrieve_patron = Mock()
        self.CuT.retrieve_patron.return_value = None
        self.assertIsNotNone(self.CuT.insert_patron(self.patron2))

    def test_get_patron_count(self):
        self.CuT.db.all.return_value = []
        self.assertEqual(0, self.CuT.get_patron_count())

    def test_get_all_patrons(self):
        self.CuT.db.all.return_value = ["test", "filler"]
        self.assertEqual(["test", "filler"], self.CuT.get_all_patrons())

    def test_update_patron_not_Patron(self):
        self.assertIsNone(self.CuT.update_patron(None))

    def test_update_patron_success(self):
        self.patron2.add_borrowed_book("test")
        self.CuT.update_patron(self.patron2)
        self.CuT.db.update.assert_called_once()

    def test_retrieve_patron_not_found(self):
        self.CuT.db.search.return_value = None
        self.assertIsNone(self.CuT.retrieve_patron(None))

    def test_retrieve_patron_success(self):
        self.CuT.db.search.return_value = [{"fname": "Reggie", "lname": "Miller", "age": 49, "memberID": "987654321", "borrowed_books": []}]
        patron = self.CuT.retrieve_patron(self.patron1)
        self.assertEqual(patron.memberID, self.patron1.memberID)


    def test_close_db(self):
        self.CuT.close_db()
        self.assertTrue(self.CuT.db.close.called)

    def test_convert_patron_to_db_format(self):
        self.assertIsNotNone(self.CuT.convert_patron_to_db_format(self.patron1))

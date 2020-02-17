import unittest
import sys
sys.path.append('../')
from library.patron import Patron
from library.patron import InvalidNameException


class TestPatron(unittest.TestCase):

#    def SetUp(self):
#        # InvalidNameException = unittest.Mock()
#        self.patron1 = Patron("first", "last", 23, "98765432")

    def test_constructor(self):
        patron = Patron("mister", "twister", 49, "yert4321")
        # constructor executed without error
        self.assertTrue(True)

    def test_constructor_numberName(self):              # MOCK EXCEPTION CLASS?
        try:
            patron = Patron("yupp", "5678", 49, "yert4321")
        except InvalidNameException:
            self.assertTrue(True)
            return
        self.assertTrue(False, "Expected InvalidNumberException")


    def test_get_memberID(self):
        ID = "yert4321"
        patron = Patron("mister", "twister", 49, ID)
        self.assertEqual(patron.get_memberID(), "yert4321")

    def test_get_age(self):
        age = 49
        patron = Patron("mister", "twister", age, "yert4321")
        self.assertEqual(patron.get_age(), 49)

    def test_get_fname(self):
        fname = "mister"
        patron = Patron(fname, "twister", 49, "yert4321")
        self.assertEqual(patron.get_fname(), "mister")

    def test_get_lname(self):
        lname = "twister"
        patron = Patron("mister", lname, 49, "yert4321")
        self.assertEqual(patron.get_lname(), "twister")

    def test_get_books(self):
        patron = Patron("first", "last", 23, "98765432")
        books = patron.get_borrowed_books()
        self.assertFalse(books, "Expected empty list")

    def test_add_new_book(self):
        book = "Lord of the Flies"
        patron = Patron("first", "last", 23, "98765432")
        patron.add_borrowed_book(book)
        self.assertEqual(patron.get_borrowed_books()[0], "Lord of the Flies".lower())

    def test_add_old_book(self):
        book = "Lord of the Flies"
        patron = Patron("first", "last", 23, "98765432")
        patron.add_borrowed_book(book)
        patron.add_borrowed_book(book)
        self.assertEqual(len(patron.get_borrowed_books()), 1)

    def test_return_book(self):
        book = "Lord of the Flies"
        patron = Patron("first", "last", 23, "98765432")
        patron.add_borrowed_book(book)
        patron.return_borrowed_book(book)
        self.assertEqual(len(patron.get_borrowed_books()), 0)

    def test_eq(self):
        patron1 = Patron("first", "last", 23, "98765432")
        patron2 = Patron("first", "last", 23, "98765432")
        self.assertTrue(patron1==patron2)

    def test_ne(self):
        patron1 = Patron("burst", "ghast", 33, "23456789")
        patron2 = Patron("first", "last", 23, "98765432")
        self.assertTrue(patron1!=patron2)


if __name__ == '__main__':
    unittest.main()

import unittest
import unittest.mock
from library.library_db_interface import Library_DB
from library.patron import Patron


class TestDBInterface(unittest.TestCase):

    def setUp(self):
        self.CuT = Library_DB()
        self.patron = unittest.mock.MagicMock()
        self.patron.memberID = "987654321"
        self.patron.age = 49
        self.patron.fname = "Reggie"
        self.patron.lname = "Miller"
        self.patron.borrowed_books = ["Old Man and the Sea"]

    def test_insert_patron(self):
        initialSize = len(self.CuT.db)
        self.CuT.insert_patron(self.patron)
        self.patron.get_memberID().assertCalled()
        finalSize = len(self.CuT.db)
        self.assertTrue(initialSize + 1 == finalSize)



if __name__ == '__main__':
    unittest.main()

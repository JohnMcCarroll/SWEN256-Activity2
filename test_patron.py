import unittest
from library.patron import Patron


class TestPatron(unittest.TestCase):
    def test_constructor(self):
        patron = Patron("mister", "twister", 49, "yert4321")
        # constructor executed without error
        self.assertTrue(True)

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



if __name__ == '__main__':
    unittest.main()

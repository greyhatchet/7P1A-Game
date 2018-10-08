import unittest
from savereader import readSave

class SaveReaderTestCase(unittest.TestCase):
    # Tests for savereader.py

    def test_readSave(self):
        self.assertTrue(readSave(0))
        self.assertTrue(not readSave(99))
        self.assertTrue(not readSave('asd'))


if __name__ == '__main__':
    unittest.main()

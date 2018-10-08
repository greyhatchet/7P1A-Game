import unittest
from savewriter import writeSave

class SaveWriterTestCase(unittest.TestCase):
    # Tests for savewriter.py

    def test_writeSave(self):
        self.assertTrue(writeSave({'a': 2}, 0))
        self.assertTrue(not writeSave({}, 1))
        self.assertTrue(not writeSave({'aa': 2}, 3))
        self.assertTrue(not writeSave('aaa', 2))



if __name__ == '__main__':
    unittest.main()
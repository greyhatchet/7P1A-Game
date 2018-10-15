import unittest
from scorewriter import writeScores

class ScoreWriterTestCase(unittest.TestCase):
    # Tests for scorewriter.py

    def test_writeScores(self):
        self.assertTrue(writeScores([('a', 2), ('b', 3)]))
        self.assertTrue(writeScores([]))
        self.assertTrue(not writeScores([1, 3, 4]))
        self.assertTrue(not writeScores('a'))


if __name__ == '__main__':
    unittest.main()

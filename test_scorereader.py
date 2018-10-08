import unittest
from scorereader import readScores

class ScoreReaderTestCase(unittest.TestCase):
    # Tests for scorereader.py

    def test_readScores(self):
        self.assertTrue(readScores('scoresfile.txt'))
        self.assertTrue(not readScores('notarealfilename.txt'))
        self.assertTrue(not readScores(4))


if __name__ == '__main__':
    unittest.main()
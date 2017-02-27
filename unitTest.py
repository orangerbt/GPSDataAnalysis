import unittest
from analysis import Analysis

class UnitTests(unittest.TestCase):

    def testGprmc(self):
        a = Analysis()
        a.main()
        self.assertEqual(len(a.gprmc), 10)
        self.assertEqual(len(a.gprmc[1]), 8)
        self.assertEqual(len(a.gprmc[7]), 10)
        self.assertEqual(a.gprmc[0], "Recommended minimum specific GPS/Transit data")
        
if __name__ == "__main__":
    unittest.main()

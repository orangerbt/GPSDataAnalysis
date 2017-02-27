import unittest
from analysis import Analysis

class UnitTests(unittest.TestCase):

    def testGprmc(self):
        a = Analysis()
        a.main()
        self.assertEqual(len(a.gprmc), 10)
        self.assertEqual(len(a.gprmc[1]), 8) # Time is 8 chars long
        self.assertEqual(len(a.gprmc[7]), 10) # Date is 10 chars long
        self.assertEqual(a.gprmc[0], "Recommended minimum specific GPS/Transit data")
    def testGpgga(self):
        a = Analysis()
        a.main()
        self.assertEqual(a.gpgga[0], "Global Positioning System Fix Data")
        self.assertEqual(len(a.gpgga), 10)
        self.assertEqual(len(a.gpgga[1]), 8) # Time is 8 chars long
        
if __name__ == "__main__":
    unittest.main()

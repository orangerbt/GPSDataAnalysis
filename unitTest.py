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
        with self.assertRaises(Exception):
            gprmcStub = [0] * 10
            # the checksum on this should be 4C, but it is 4D
            lineStub = ['$GPRMC', '220711.225', 'V', '', '', '', '', '0.00',
                        '0.00', '160217', '', '', 'N*4D\r\n'] 
            a.gprmcParse(gprmcStub, lineStub) 
                         
    def testGpgga(self):
        a = Analysis()
        a.main()
        self.assertEqual(a.gpgga[0], "Global Positioning System Fix Data")
        self.assertEqual(len(a.gpgga), 10)
        self.assertEqual(len(a.gpgga[1]), 8) # Time is 8 chars long

        with self.assertRaises(Exception):
            gpggaStub = [0] * 10
            # the checksum on this should be 65, but it is 6D
            lineStub = ['$GPGGA', '220818.000', '4302.2807', 'N', '07607.9369',
                        'W', '1', '6', '4.18', '181.8', 'M', '-34.0', 'M', '',
                        '*6D\r\n']
            a.gpggaParse(gpggaStub, lineStub)

    def testGpgll(self):
        a = Analysis()
        a.main()
        self.assertEqual(a.gpgll[0], "Geographic position, Latitude and Longitude")
        self.assertEqual(len(a.gpgll), 6)
       
        
        with self.assertRaises(Exception):
            gpgllStub = [0] * 6
            # the checksum on this should be 70, but it is 71
            lineStub = ["$GPGLL","","","","","220651.080","V","N*71\r\n"] 
            a.gpgllParse(gpgllStub,lineStub)


    def testGpvtg(self):
	a = Analysis()
	a.main()
	self.assertEqual(a.gpvtg[0], "Track Made Good and Ground Speed")
	self.assertEqual(len(a.gpvtg), 6)

	with self.assertRaises(Exception):
	    gpvtgStub = [0] * 6
	    # the checksum on this should be 3E, but it is 4E
	    lineStub = ["$GPVTG","176.74","T","","M","0.00","N","0.00","K","A*4E"]
	    a.gpvtgParse(gpvtgStub,lineStub)

    def testGpgsa(self):
        a = Analysis()
        a.main()
        self.assertEqual(a.gpgsa[0], "GPS DOP and active satellites")
        self.assertEqual(len(a.gpgsa), 8)

        with self.assertRaises(Exception):
            gpgsaStub = [0] * 8
            # the checksum on this should be 1E, but it is 1C
            lineStub = ['GPS DOP and active satellites', 'Automatic', 'No Fix',
                        ['', '', '', '', '', '', '', '', ''], '', '', '',
                        '*1C\r\n']
            a.gpgsaParse(gpgsaStub, lineStub)

if __name__ == "__main__":
    unittest.main()

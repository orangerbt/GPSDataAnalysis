class Analysis:

    # Initialize the class variables
    def __init__(self):
        self.gprmc = [0] * 10
        self.gprmc[0] = "Recommended minimum specific GPS/Transit data"
        self.gpgga = [0] * 10
        self.gpgga[0] = "Global Positioning System Fix Data"
        self.gpgll = [0] * 6
        self.gpgll[0] = "Geographic position, Latitude and Longitude"
        self.gpvtg = [0] * 6
        self.gpvtg[0] = "Track Made Good and Ground Speed"

    def main(self):
        infile = open("gnss.txt", "r")
        lines = infile.readlines()
        
        for line in lines:
            line = line.split(",")

            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)
            if line[0] == "$GPGGA":
                self.gpgga = self.gpggaParse(self.gpgga, line)
            if line[0] == "$GPGLL":
                self.gpgll = self.gpgllParse(self.gpgll, line)
            if line[0] == "$GPVTG":
                self.gpvtg = self.gpvtgParse(self.gpvtg, line)

   

    '''
    GPRMC properties

    gprmc[0] - "Recommended minimum specific GPS/Transit data"
    gprmc[1] - Time of fix, UTC
    gprmc[2] - Navigation receiver warning (either OK or WARNING)
    gprmc[3] - Latitude, in degrees (+ indicates North, - indicates South)
    gprmc[4] - Longitude, in degrees (+ indicates East, - indicates West)
    gprmc[5] - Speed over ground (in knots)
    gprmc[6] - Course (in degrees)
    gprmc[7] - Date of fix, YY/MM/DD
    gprmc[8] - Magnetic variation, format: [degrees, cardinal direction]
    gprmc[9] - Checksum
    '''

    def gprmcParse(self, gprmc, line):
        gprmc[1] = line[1][0:2] + ":" + line[1][2:4] + ":" + line[1][4:6]
        gprmc[2] = "OK" if line[2] == "A" else "WARNING"

        directionLat = "+" if line[4] == "N" else "-"
        if line[3] != "":
            latitude = float(line[3][:-5] + (float(line[3][-5:]) / 60))
        else:
            latitude = 0.0
        gprmc[3] = directionLat + str(latitude)

        directionLong = "+" if line[6] == "E" else "-"
        if line[5] != "":
            longitude = float(line[5][:-5] + (float(line[3][-5:]) / 60))
        else:
            longitude = 0.0
        gprmc[4] = directionLong + str(longitude)

        gprmc[5] = line[7]
        gprmc[6] = line[8]
        
        year = ("20" if float(line[9][4:6]) < 50 else "19") + line[9][4:6]
        gprmc[7] = year + "-" + line[9][0:2] + "-" + line[9][2:4]
        
        directionMag = "+" if line[11] == "E" else "-"
        gprmc[8] = directionMag + line[10]
        
        gprmc[9] = line[12]
        
        if self.verifyChecksum(line, gprmc[9]):
            return gprmc

    '''
    GPGGA Properties

    gpgga[0] - "Global Positioning System Fix Data"
    gpgga[1] - Time of position, UTC
    gpgga[2] - Latitude of position, in degrees (North +, South -)
    gpgga[3] - Longitude of position, in degrees (East +, West -)
    gpgga[4] - GPS Fix data
    gpgga[5] - Number of satellites in view
    gpgga[6] - Horizontal Dilution of Precision, how accurate the horizontal position is
    gpgga[7] - Altitude, the height above mean sea level and the units (F = feet, M = meters)
    gpgga[8] - Height of the geoid above WGS84 Ellipsoid with units (F = feet, M = meters)
    gpgga[9] - Checksum
    '''

    def gpggaParse(self, gpgga, line):
        gpgga[1] = line[1][0:2] + ":" + line[1][2:4] + ":" + line[1][4:6]
        directionLat = "+" if line[3] == "N" else "-"
        if line[2] != "":
            latitude = float(float(line[2][:-7]) + (float(line[2][-7:]) / 60))
        else:
            latitude = 0.0
        gpgga[2] = directionLat + str(latitude)
        directionLon = "+" if line[5] == "E" else "-"
        if line[4] != "":
            longitude = float(float(line[4][:-7]) + (float(line[4][-7:]) / 60))
        else:
            longitude = 0.0
        gpgga[3] = directionLon + str(longitude)
        if line[6] == "0":
            gpgga[4] = "Invalid"
        elif line[6] == "1":
            gpgga[4] = "GPS Fix"
        else:
            gpgga[4] = "DGPS Fix"
        gpgga[5] = line[7]
        gpgga[6] = line[8]
        gpgga[7] = line[9] + line[10]
        gpgga[8] = line[11] + line[12]
        gpgga[9] = line[14]
        
        if self.verifyChecksum(line, gpgga[9]):
            return gpgga

        '''
        GPGLL Properties

        gpgll[0] - "Geographic position, Latitude and Longitude"
        gpgll[1] - Latitude of position, in degrees (North +, South -)
        gpgll[2] - Longitude of position, in degrees (East +, West -)
        gpgll[3] - Time of position, UTC
        gpgll[4] - Data Active or V (void)
        gpgll[5] - checksum data

        '''        

    def gpgllParse(self, gpgll, line):
         if line[1] != "":
            latitude = float(float(line[1][:-5]) + (float(line[1][-5:]) / 60))
         else:
            latitude = 0.0
         directionLat = "+" if line[2] == "N" else "-"
         gpgll[1] = directionLat + str(latitude)
         if line[3] != "":
            longitude = float(float(line[3][:-5]) + (float(line[3][-5:]) / 60))
         else:
            longitude = 0.0
         directionLong = "+" if line[4] == "E" else "-"
         gpgll[2] = directionLong + str(longitude)
         gpgll[3] = line[5][0:2] + ":" + line[5][2:4] + ":" + line[5][4:6]
         gpgll[4] = "Data Active" if line[6] == "A" else "Void" 
         gpgll[5] = line[7]
         if self.verifyChecksum(line, gpgll[5]):
             return gpgll


 	 '''

    	 GPVTG properties
    
   	 gpvtg[0] - "Track Made Good and Ground Speed"
  	 gpvtg[1] - True track made good
   	 gpvtg[2] - Magnetic track made good
   	 gpvtg[3] - Ground speed, knots
   	 gpvtg[4] - ground speed, Kimometers per hour
   	 gpvtg[5] - Checksum

   	 '''

    def gpvtgParse(self, gpvtg, line):
         gpvtg[1] = line[1] + line[2]
         gpvtg[2] = ("0.00" if line[3] == "" else line[3])+line[4]
         gpvtg[3] = line[5] + line[6]
         gpvtg[4] = line[7] + line[8]
	 gpvtg[5] = line[9]
         if self.verifyChecksum(line, gpvtg[5]):
             return gpvtg

    def verifyChecksum(self, line, checksum):
        # Take the entire sentence string and remove the initial $ and the * and everything after it
        sumString = ",".join(line)[1:-5]
        calculatedSum = 0
        for char in sumString:
            calculatedSum = calculatedSum ^ ord(char)
        checksum = checksum.split("*",1)[1]
        checksum = checksum[:-2]

        # int(string, 16) translates a string representing a hexidecimal number to a decimal integer.
        # For example, int("4C", 16) returns 76.
        if int(checksum, 16) == calculatedSum:
            return True
        else:
            raise Exception("Checksum is incorrect! \n" +
                            "Expected " + checksum + ", calculated " + str(hex(calculatedSum)) + "\n"
                            "when parsing line: " + str(line))
        return int(checksum, 16) == calculatedSum


    
if __name__ == "__main__":
    Analysis().main()

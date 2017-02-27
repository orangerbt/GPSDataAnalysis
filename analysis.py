class Analysis:

    # Initialize the class variables
    def __init__(self):
        self.gprmc = [0] * 10
        self.gprmc[0] = "Recommended minimum specific GPS/Transit data"
        self.gpgga = [0] * 10
        self.gpgga[0] = "Global Positioning System Fix Data"

    def main(self):
        infile = open("gnss.txt", "r")
        lines = infile.readlines()
        
        for line in lines:
            line = line.split(",")

            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)
            if line[0] == "$GPGGA":
                self.gpgga = self.gpggaParse(self.gpgga, line)


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
        
        return gprmc


'''
GPGGA Properties

gpgga[0] - Global Positioning System Fix Data
gpgga[1] - Time of position, UTC
gpgga[2] - Latitude of position, in degrees
gpgga[3] - Orientation, North (+) or South (-)
gpgga[4] - Longitude of position, in degrees
gpgga[5] - Orientation, East (+) or West (-)
gpgga[6] - GPS Fix data
gpgga[7] - Number of satellites in view
gpgga[8] - Horizontal Dilution of Precision, how accurate the horizontal position is
gpgga[9] - Altitude, the height above mean sea level and the units (feet, meters)
gpgga[10] - Height of the geoid above WGS84 Ellipsoid with units (feet, meters)
gpgga[11] - Time since last DGPS update
gpgga[12] - DGPS reference station id
gpgga[13] - Checksum
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
        gpgga[9] = line[13]
        print(gpgga)
        return gpgga

if __name__ == "__main__":
    Analysis().main()

class Analysis:

    # Initialize the class variables
    def __init__(self):
        self.gprmc = [0] * 10
        self.gprmc[0] = "Recommended minimum specific GPS/Transit data"
        
    def main(self):
        infile = open("gnss.txt", "r")
        lines = infile.readlines()
        
        for line in lines:
            line = line.split(",")

            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)


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

if __name__ == "__main__":
    Analysis().main()

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
    gprmc[3] - Latitude, format: [degrees, minutes, cardinal direction]
    gprmc[4] - Longitude, format: [degrees, minutes, cardinal directon]
    gprmc[5] - Speed over ground (in knots)
    gprmc[6] - Course Made Good
    gprmc[7] - Date of fix, YY/MM/DD
    gprmc[8] - Magnetic variation, format: [degrees, cardinal direction]
    gprmc[9] - Checksum
    '''

    def gprmcParse(self, gprmc, line):
        gprmc[1] = line[1][0:2] + ":" + line[1][2:4] + ":" + line[1][4:6]
        gprmc[2] = "OK" if line[2] == "A" else "WARNING"

        gprmc[3] = [line[3][-4:]]
        line[3] = line[3][-4:]
        gprmc[3].append(line[3])
        gprmc[3].append(line[4])

        gprmc[4] = [line[5][-4:]]
        line[5] = line[5][-4:]
        gprmc[4].append(line[5])
        gprmc[4].append(line[6])

        gprmc[5] = line[7]
        gprmc[6] = line[8]
        gprmc[7] = line[9][4:6] + "/" + line[9][0:2] + "/" + line[9][2:4]
        gprmc[8] = [line[10], line[11]]
        gprmc[9] = line[12]

        return gprmc

if __name__ == "__main__":
    from unitTest import unittest
    unittest.main()

class Analysis:
    '''
    lock
    lat/longitud
    time


    gpgsa - dilution
    gprmc - latlong/time/
    gpgga - altitude/fix
    '''
    # Initialize the class variables
    def __init__(self):
        self.gprmc = [0] * 10
        self.gprmc[0] = "gprmc"

    def parseRT(self,data):
        output = []
        outputString = ""

        for line in data:
            line = line.split(",")
            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)
                output.append(self.gprmc)
                outputString+='$' + ','.join(self.gprmc)

        print(outputString)
        #print("GPRMC: "+str(self.gprmc))
        return output

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
            latitude = float(line[3][:2]) + (float(line[3][2:4])/60) + (float(line[3][5:])/60/60)
        else:
            latitude = 0.0
        gprmc[3] = directionLat + str(latitude)
        directionLong = "+" if line[6] == "E" else "-"
        if line[5] != "":
            longitude = float(line[5][:3]) + (float(line[5][3:5])/60) + (float(line[5][6:])/60/60)
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
        print(gprmc[9])

        if self.verifyChecksum(line, gprmc[9]):
            return gprmc

    def verifyChecksum(self, line, checksum):
        # Take the entire sentence string and remove the initial $ and the * and everything after it
        sumString = ",".join(line)[1:-4]#-5
        calculatedSum = 0
        for char in sumString:
            calculatedSum = calculatedSum ^ ord(char)
        checksum = checksum.split("*",1)[1]
        checksum = checksum[:-1]

        # int(string, 16) translates a string representing a hexidecimal number to a decimal integer.
        # For example, int("4C", 16) returns 76.
        if int(checksum, 16) == calculatedSum:
            return True
        else:
            raise Exception("Checksum is incorrect! \n" +
                            "Expected " + checksum + ", calculated " + str(hex(calculatedSum)) + "\n"
                            "when parsing line: " + str(line))
        return int(checksum, 16) == calculatedSum


'''
if __name__ == "__main__":
    output = Analysis().main()
'''

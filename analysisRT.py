class Analysis:
    '''
    lock
    lat/longitud
    time


    gpgsa - dilution 4
    gprmc - latlong/time/speed/course 3,4,5,6
    gpgga - altitude/fix 7
    '''
    # Initialize the class variables
    def __init__(self):
        self.gprmc = [0] * 10
        self.gprmc[0] = "gprmc"
        self.gpgga = [0] * 10
        self.gpgga[0] = "gpggga"
        self.gpgsa = [0] * 8
        self.gpgsa[0] = "gpgsa"

    def parseRT(self,data):
        output = []
        outputString = ""

        for line in data:
            line = line.decode("utf-8").split(",")
            print(line)
            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)
                #output.append(self.gprmc)
                outputString+='$' + ','.join(self.gprmc[3:6])
                output.append(outputString)
            if line[0] == "$GPGSA":
                self.gpgsa = self.gpgsaParse(self.gpgsa, line)
                outputString+= "," + self.gpgsa[4]
                output.append("output = " + outputString)
                print(outputString)
                outputString = ""
            if line[0] == "$GPGGA":
                gpgga = self.gpggaParse(self.gpgga, line)
                outputString+= "," + self.gpgga[7]

        #print(outputString)
        #print("GPRMC: "+str(self.gprmc))
        for o in output:
            print("o = " + str(o) + "\n")
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
    GPGSA properties

    gpgsa[0] - "GPS DOP and active satellites"
    gpgsa[1] - selection of 2D or 3D fix, A for auto, M for manual
    gpgsa[2] - Fix dimensions, 1 for no fix, 2 for 2D fix, 3 for 3D fix
    gpgsa[3] - List of PRNs of satellites used for fix (space for 12)
    gpgsa[4] - PDOP (dilution of precision)
    gpgsa[5] - Horizontal dilution of precision (HDOP)
    gpgsa[6] - Vertical dilution of precision (VDOP)
    gpgsa[7] - Checksum

    '''
    def gpgsaParse(self, gpgsa, line):
        gpgsa[1] = "Automatic" if line[1] == "A" else "Manual"

        if line[2] == "1":
            gpgsa[2] = "No Fix"
        elif line[2] == "2":
            gpgsa[2] = "2D Fix"
        elif line[2] == "3":
            gpgsa[2] = "3D Fix"
        else:
            gpgsa[2] = "Fix not defined"

        gpgsa[3] = line[4:13]
        gpgsa[4] = line[14]
        gpgsa[5] = line[15]
        gpgsa[6] = line[16]
        gpgsa[7] = line[17]

        if self.verifyChecksum(line, gpgsa[7]):
            return gpgsa


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

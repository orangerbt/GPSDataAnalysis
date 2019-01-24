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
        self.gpgsa = [0] * 8
        self.gpgsa[0] = "GPS DOP and active satellites"
        self.gpgsv = [0] * 9
        self.gpgsv[0] = "GPS Satellites in View"

    def main(self):
        infile = open("test1", "r")
        outfile = open("output.txt","w")
        lines = infile.readlines()

        for line in lines:
            line = line.split(",")
            if line[0] == "$GPRMC":
                self.gprmc = self.gprmcParse(self.gprmc, line)
                outfile.write(str(self.gprmc) + "\n")
            if line[0] == "$GPGGA":
                self.gpgga = self.gpggaParse(self.gpgga, line)
                outfile.write(str(self.gpgga) + "\n")
            if line[0] == "$GPGLL":
                self.gpgll = self.gpgllParse(self.gpgll, line)
                outfile.write(str(self.gpgll) + "\n")
            if line[0] == "$GPVTG":
                self.gpvtg = self.gpvtgParse(self.gpvtg, line)
                outfile.write(str(self.gpvtg) + "\n")
            if line[0] == "$GPGSA":
                self.gpgsa = self.gpgsaParse(self.gpgsa, line)
                outfile.write(str(self.gpgsa) + "\n")
            if line[0] == "$GPGSV":
                self.gpgsv = self.gpgsvParse(self.gpgsv, line)
                outfile.write(str(self.gpgsv) + "\n")


        print("GPRMC: "+str(self.gprmc))
        print("GPGGA: "+str(self.gpgga))
        print("GPGLL: "+str(self.gpgll))
        print("GPVTG: "+str(self.gpvtg))
        print("GPGSA: "+str(self.gpgsa))
        print("GPGSV: "+str(self.gpgsv))
        outfile.close()



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
    gpvtg[4] - ground speed, Kilometers per hour
    gpvtg[5] - Checksum

    '''

    def gpvtgParse(self, gpvtg, line):
         gpvtg[1] = line[1] + line[2]
	 #The data we recive for this field can be empty, so we chekc for it being empty here and insert 0.00 if it is
         gpvtg[2] = ("0.00" if line[3] == "" else line[3])+line[4]
         gpvtg[3] = line[5] + line[6]
         gpvtg[4] = line[7] + line[8]
         gpvtg[5] = line[9]
         if self.verifyChecksum(line, gpvtg[5]):
             return gpvtg

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

    '''
    GPGSV properties

    gpgsv[0] - "GPS Satellites in View"
    gpgsv[1] - Number of sentences for full data
    gpgsv[2] - The sentence number
    gpgsv[3] - The number of satellites in view
    gpgsv[4] - Information on satelite in view
               [Information on Satellite PRN number; Elevation in  degrees,
               90 maximum; Azimuth, degrees from true north, 000 to 359;
               SNR 00-99db (null when not tracking)]
    gpgsv[5] - Information about second SV, same as gpgsv[4]
    gpgsv[6] - Information third second SV, same as gpgsv[4]
    gpgsv[7] - Information fourth second SV, same as gpgsv[4]
    gpgsv[8] - Checksum
    *Depending on the amount of satellites in view, gpgsv[5-7] may not exist.
    In that case, the location of the checksum is gpgsv[len(gpgsv)-1]
    '''

    def gpgsvParse(self, gpgsv, line):
        del gpgsv[1:]
        gpgsv.append(line[1])
        gpgsv.append(line[2])
        gpgsv.append(line[3])
        #checks to see if the data is complete/error free
        if not line[3].isdigit():
            return gpgsv
        #calculates the amount of satellites in previous sentences
        prevSV = (int(line[2])-1)*4
        #calculates the amount of satellites in view in the current sentence
        amtSV = int(float(line[3]) - prevSV)
        if amtSV > 4:
            amtSV = 4
        #appending lists of data for satellites in view
        for x in (range(4,4+amtSV*4,4)):
            if x == (amtSV*4):
                foo = line[x:x+3]
                foo.append(line[x+3][:-5])
                gpgsv.append(foo)
            else:
                gpgsv.append(line[x:x+4])
        #checksum
        gpgsv.append(line[len(line)-1])
        if self.verifyChecksum(line,gpgsv[len(gpgsv)-1]):
            return gpgsv

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

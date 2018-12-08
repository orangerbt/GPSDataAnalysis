import udp
import serial
import analysisRT

class Parse:
    # Initialize the class variables
    def __init__(self):
        self.holding = ""
        self.buffer = [0] * 10


    def main(self):
        send = udp.UDP()
        send.createIdentificationFile()
        ser1 = serial.Serial('/dev/pts/18',19200, rtscts=True,dsrdtr=True)
        ser2 = serial.Serial('/dev/pts/19',19200,rtscts=True,dsrdtr=True,timeout=2)
        while True:
            data = self.read(ser1,ser2)
            parsedData = self.analyze(data)
            self.send(send,parsedData)

    def read(self,ser1,ser2):

         # open serial port

        print(ser1.name)
        '''
        infile = open("gnss.txt", "r")
        lines = infile.readlines()

        for line in lines:
            print(line)
            ser1.write(line.encode())
        '''
        #seq = '$GPRMC,220652.080,V,,,,,0.00,0.00,160217,,,N*47'
        #ser1.write('{!r}'.format(seq))
        #ser1.write('$GPRMC,220652.080,V,,,,,0.00,0.00,160217,,,N*47'.encode())
        #ser1.write('$GPRMC,220651.080,V,,,,,0.00,0.00,160217,,,N*44\n')
        #{!r}'.format(seq)
        #ser1.write('$world\n')
        print("read lines\n")
        line = ser2.readlines()
        if (len(line) > 2):
            print("data received\n")
        #print(line)
        print("return line\n")
        return line
        #do reading stuff
        #return line

    def analyze(self,data):
        import analysisRT
        art = analysisRT.Analysis()
        '''
        dataRet = []
        for d in data:
            #print(d)
            dataRet.append(art.parseRT(d))
        #data = art.parseRT(data)
        #print(data)
        return data
        '''
        return art.parseRT(data)

    def send(self,send,data):
        for d in data:
            #print("The datatype is: " + str(d))
            send.sendMessage(d)
            #print(d)
        #do sending stuff
        return

if __name__ == "__main__":

    Parse().main()

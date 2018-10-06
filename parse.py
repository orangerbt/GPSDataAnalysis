import udp
import serial

class Parse:
    # Initialize the class variables
    def __init__(self):
        self.holding = ""
        self.buffer = [0] * 10


    def main(self):
        send = udp.UDP()
        send.createIdentificationFile()

        data = self.read()
        parsedData = self.analyze(data)
        self.send(send,parsedData)

    def read(self):

        ser1 = serial.Serial('/dev/pts/5',19200, rtscts=True,dsrdtr=True)  # open serial port
        ser2 = serial.Serial('/dev/pts/18',19200,rtscts=True,dsrdtr=True,timeout=2)
        print(ser1.name)
        seq = '$GPRMC,220652.080,V,,,,,0.00,0.00,160217,,,N*47\n'
        #ser1.write('{!r}'.format(seq))
        ser1.write('$GPRMC,220652.080,V,,,,,0.00,0.00,160217,,,N*47\n'.encode())
        #ser1.write('$GPRMC,220651.080,V,,,,,0.00,0.00,160217,,,N*44\n')
        #{!r}'.format(seq)
        #ser1.write('$world\n')
        line = ser2.readlines()

        return line
        #do reading stuff
        #return line

    def analyze(self,data):
        import analysisRT
        art = analysisRT.Analysis()
        #data = art.parseRT(data)
        #print(data)
        return data

    def send(self,send,data):
        for d in data:
            send.sendMessage(data)
            print(d)
        #do sending stuff
        return

if __name__ == "__main__":

    Parse().main()

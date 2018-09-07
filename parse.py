class Parse:

    # Initialize the class variables
    def __init__(self):
        self.holding = ""
        self.buffer = [0] * 10


    def main(self):
        import Analysis as analyze

        data = self.read()
        parsedData = self.analyze(data)
        self.send(parsedData)

    def read(self):
        import serial
        ser1 = serial.Serial('/dev/pts/11',19200, rtscts=True,dsrdtr=True)  # open serial port
        ser2 = serial.Serial('/dev/pts/20',19200,rtscts=True,dsrdtr=True,timeout=2)
        print(ser1.name)
        ser1.write('hello')
        ser1.write('world')
        line = ser2.readlines()
        #do reading stuff

    def send(self,data):
        #do sending stuff


if __name__ == "__main__":
    Parse().main()

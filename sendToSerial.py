import serial
ser1 = serial.Serial('/dev/pts/18',19200, rtscts=True,dsrdtr=True)
infile = open("gnss.txt", "r")
lines = infile.readlines()

for line in lines:
    print(line)
    ser1.write(line.encode())

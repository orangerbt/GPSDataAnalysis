import serial

ser1 = serial.Serial('/dev/pts/11',19200, rtscts=True,dsrdtr=True)  # open serial port
ser2 = serial.Serial('/dev/pts/20',19200,rtscts=True,dsrdtr=True,timeout=2)
print(ser1.name)
ser1.write('hello')
ser1.write('world')
line = ser2.readlines()
print(line)

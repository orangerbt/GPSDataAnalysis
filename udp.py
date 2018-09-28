class UDP:

    # Initialize the class variables
    def __init__(self):
        self.id = "5"
        self.desc = "GPS Data 1"
        self.ip = "localhost"
        self.port = 2222
        self.unit = "GPS data unit"


    def createIdentificationFile(self):
        content = bytearray(b'\x00\x00\x00\x00')
        #content = bytearray('','utf-8')
        identificationMessage = self.desc
        bID = (self.id).encode("utf8")
        #Extending ID to 4 bytes
        byteID = int(bID).to_bytes(4, byteorder = 'big')
        bDesc = (self.desc).encode("utf8")

        #length for DAL
        lengthIdDesc = (len(bDesc)+4).to_bytes(4, byteorder = 'big')
        content.extend(lengthIdDesc)

        #unit
        bUnit = (self.unit).encode("utf8")
        #byteUnit = int(bUnit).to_bytes(4, byteorder = 'big')

        #length for TL
        lengthUnit = (len(bUnit)).to_bytes(4, byteorder = 'big')
        print(bUnit)
        print(len(bUnit))
        print(lengthUnit)
        content.extend(lengthUnit)


        import socket
        #ID + DESC
        content.extend(byteID + bDesc)
        content.extend(bUnit)
        print(content)
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

        sock.sendto(content, (self.ip, self.port))
        return




if __name__ == "__main__":
    output = UDP()
    output.createIdentificationFile()

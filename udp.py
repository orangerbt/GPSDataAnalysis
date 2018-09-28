class UDP:

    # Initialize the class variables
    def __init__(self):
        self.id = "5"
        self.desc = "GPS Data 1"
        self.ip = "localhost"
        self.port = 2222
        self.unit = "GPS data unit"

    def createIdentificationFile(self):
        #master byte array
        content = bytearray(b'\x00\x00\x00\x00')

        #id and description
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

        #length for TL
        lengthUnit = (len(bUnit)).to_bytes(4, byteorder = 'big')
        content.extend(lengthUnit)

        #Add id + desc to content
        content.extend(byteID + bDesc)
        content.extend(bUnit)

        #actually sending the message
        self.sendMessage(content)

        return

    def sendMessage(self,byteArray):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(byteArray, (self.ip, self.port))

if __name__ == "__main__":
    import socket
    output = UDP()
    output.createIdentificationFile()

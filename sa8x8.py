import serial
import time

class sa8x8:
    def __init__(self,comport,baud=9600):
        self.port_name = comport
        self.baud_rate = baud
        self.connected=False
        self.hasMemories = False
        self.memories =[]
        self.channels=[]
        self.txSubAudio = 0
        self.rxSubAudio = 0
        self.squelch = 0


    def connect(self):

        try:
            self.ser = serial.Serial(self.port_name, self.baud_rate, bytesize=8, parity='N', stopbits=1, timeout=1)
            self.connected = True
            # self.ser.timeout=5000
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port_name}: {e}")
            return

    def send(self, tCommand):
        if self.connected:
            self.ser.write(tCommand.encode('ascii'))

            # Wait a little for the response to be received
            time.sleep(0.5)
        else:
            return -1

    def read(self):
        if self.connected:
            response = self.ser.read_until(b"\r\n")
            buf = response.decode('ascii', errors='replace')

            buf = buf.strip()
            if buf.startswith("AA"):
                buf = buf[2:]
                return buf

            else:
                return buf
        else:
            return -1

    def chipset(self):
        if self.connected:

            self.send("AT+DMOCONNECT\r\n")
            retval = self.read()
            if retval == 'ERROR':

                self.send("AAFAA\r\n")
                retval = self.read()
                if len (retval) == 0:
                    retval= -1
                if retval.startswith("SA828_"):
                    retval = "SA828"
            elif retval.startswith("+DMOCONNECT"):
                    retval = "SA818"
            else:
                    retval = -1
            return retval

    def close(self):
        if self.connected:
            self.ser.close()
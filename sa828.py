#sa828 programming script written by Frank Barton, g7wap



import serial
import time
import re
class sa828:
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
            self.ser.timeout=5000
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port_name}: {e}")
            return

    def send(self,tCommand):
        if self.connected:
            self.ser.write(tCommand.encode('ascii'))

        # Wait a little for the response to be received
            time.sleep(0.5)
        else :
            return -1
    def read(self):
        if self.connected:
            response = self.ser.read_until(b"\r\n")
            buf = response.decode('ascii', errors='replace')

            buf =buf.strip()
            if buf.startswith("AA"):
                buf=buf[2:]
                return buf

            else:
                return buf
        else:
            return -1
    def close(self):
        if self.connected:
            self.ser.close()

    def version(self):
        if self.connected:
            self.send("AAFAA\r\n")
            return self.read()

    def read_memories(self):
        if self.connected:
            self.send("AAFA1\r\n")
            buf = self.read()
            if ',' in buf:
                self.memories = buf.split(",")
                self.channels=self.memories[0:32] # returns 32 memories, tx and rx of each channel
                self.txSubAudio=self.memories[32]
                self.rxSubAudio=self.memories[33]
                self.squelch=self.memories[34]
                self.hasMemories=True


                return self.memories

        else:
            return -1

    def write_memories(self):
        if self.connected:
            pass
        else:
            return -1

    def write_file(self):
        if self.connected and self.hasMemories:
            pass
        else:
            return -1
        

#sa828 programming script written by Frank Barton, g7wap
from os import path

from sa8x8 import sa8x8

import re
class sa828(sa8x8):
    def __init__(self,comport,baud=9600):
      super().__init__(comport,baud)





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
    def read_file(self,tFilename):
        self.channels.clear()

        if path.exists(tFilename):
            file = open(tFilename,mode="r")
            line=file.readline()
            if line.strip() == "Tx;Rx":
                for lines in range (0,16):
                    line=file.readline()
                    tx,rx=line.strip().split(';')
                    self.channels.append(tx)
                    self.channels.append(rx)
                line = file.readline()
                if line.strip() == "Tone TX;Tone RX":
                    self.txSubAudio, self.rxSubAudio=file.readline().strip().split(";")

                line = file.readline().strip()
                if line.startswith("Squelch"):
                    self.squelch,_=file.readline().strip().split(';')

                self.hasMemories=True
            file.close()
        pass

    def write_file(self,tFilename):
        if self.hasMemories: # and self.connected :

            file = open(tFilename, mode="w")
            file.write("Tx;Rx\n")
            for lines in range(0, 31,2):
                chn = f"{self.channels[lines]};{self.channels[lines+1]}\n"
                file.write(chn)
            file.write("Tone TX;Tone RX\n")

            file.write(f"{self.txSubAudio};{self.rxSubAudio}\n")

            file.write("Squelch;\n")
            file.write(self.squelch+";\n")

            file.close()

        else:
            return -1
        

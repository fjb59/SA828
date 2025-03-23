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

    def read_memories(self,dumpfile=None):
        if self.connected:
            self.send("AAFA1\r\n")
            buf = self.read()
            if dumpfile is not None:
                debug=open(dumpfile,mode="w")
                debug.write(buf)
                debug.close()
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

        # AAFA3409.7500,409.7500,410.7500,410.7500,411.7500,411.7500,412.7500,412.7500,413.7500,413.7500,414.7500,414.7500,415.7500,415.7500,416.7500,416.7500,417.7500,417.7500,418.7500,418.7500,419.7500,419.7500,420.7500,420.7500,421.7500,421.7500,422.7500,422.7500,423.7500,423.7500,424.7500,424.7500,000,000,1 working
        # AAFA3433.0150,433.0150,433.0300,433.0300,433.0450,433.0450,433.0600,433.0600,433.0750,433.0750,433.0900,433.0900,433.1050,433.1050,433.1200,433.1200,433.1350,433.1350,433.1500,433.1500,433.1650,433.1650,433.1800,433.1800,433.1950,433.1950,433.2100,433.2100,433.2250,433.2250,433.2400,433.2400,4,4,1
        if self.connected:
            buf=""
            for lines in range(0, 31, 2):
                buf = buf + f"{self.channels[lines]},{self.channels[lines + 1]},"


            cmd = "AAFA3"+buf
            self.send(cmd+f"{self.txSubAudio.zfill(3)},{self.rxSubAudio.zfill(3)},{self.squelch}\r\n")
            resonse = self.read()
            print (resonse)
            pass
        else:
            return -1
    def reset(self,tSure =False):
        if tSure:
            self.send("AAFA2\r\n")
            response = self.read()
            pass

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
        if self.hasMemories and self.connected :

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
        

import glob
import sa828


def main():
    files = glob.glob("".join(["/dev/tty.", "usbserial*"]))
    if len(files) >0:
        port = files[0]
        myradio=sa828.sa828(port,9600)
        # Replace 'COM3' with your actual serial port (e.g. '/dev/ttyUSB0' on Linux)

        myradio.connect()
        if myradio.connected:
            if myradio.chipset() == "SA828":
                myradio.read_memories(dumpfile="/Users/frank/Documents/sa828-memories.txt")
               # myradio.read_file("/Users/frank/Documents/sa828-memories.csv")

                #myradio.write_memories()

                myradio.write_file("/Users/frank/Documents/sa828-memories_.csv")



        # Write command to serial port (encoded as ASCII)

        # Read available bytes (adjust the number of bytes or timresponse = myradio.read()

        # Decode and display the response


        myradio.close()


if __name__ == '__main__':
    main()

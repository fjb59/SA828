import glob
import sa828


def main():

        myradio=sa828.sa828()
        myradio.read_file("/Users/frank/Documents/sa828-memories-repeaters.csv")

        myradio.connect()
        if myradio.connected:
            if myradio.chipset() == "SA828":
                myradio.read_memories(dumpfile="/Users/frank/Documents/sa828-memories.txt")


                #myradio.write_memories()

                myradio.write_file("/Users/frank/Documents/sa828-memories_.csv")



        # Write command to serial port (encoded as ASCII)

        # Read available bytes (adjust the number of bytes or timresponse = myradio.read()

        # Decode and display the response


        myradio.close()


if __name__ == '__main__':
    main()

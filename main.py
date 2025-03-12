import serial
import time
import sa828


def main():
    myradio=sa828.sa828("/dev/tty.usbserial-14630",9600)
    # Replace 'COM3' with your actual serial port (e.g. '/dev/ttyUSB0' on Linux)
    myradio.connect()
    if myradio.connected:
       myradio.read_memories()

    # Write command to serial port (encoded as ASCII)

    # Read available bytes (adjust the number of bytes or timeout as needed)
    response = myradio.read()

    # Decode and display the response


    myradio.close()


if __name__ == '__main__':
    main()

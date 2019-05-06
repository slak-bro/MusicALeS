import serial
from struct import pack
from enum import Enum
import numpy as np
import time
class Command(Enum):
    SETUP = 97
    LIGHT = 1

class Driver(object):
    def __init__(self, dev="/dev/ttyS2", baud_rate=500000):
        self.serial = serial.Serial(dev, baud_rate)
        self.nLeds = None
    def setup(self, nLeds):
        self.nLeds = nLeds
        self.serial.write(pack('<B', Command.SETUP.value))
        self.serial.flush()
        # print(self.serial.readline())
        self.serial.write(pack('<BB', nLeds//256, nLeds%256))
        self.serial.flush()
        print(self.serial.readline())

    def light(self, data):
        """[summary]
        
        Args:
            data ([np array]): shape: nLeds,3
        """

        self.serial.write(pack('<B', Command.LIGHT.value))
        self.serial.flush()
        self.serial.read()
        d = list(data.flatten())
        #print(self.serial.readline())
        self.serial.write(pack("<{}B".format(3*self.nLeds), *d))
        self.serial.flush()
        self.serial.read()

if __name__ == "__main__":
    d = Driver()
    nled = 300
    d.setup(nled)
    i=0
    print("Setup complete.")
    N = 500
    start = time.time()
    while i < N:
        a = np.array([[255,(i%2)*255,255]]*nled)
        d.light(a)
        i+=1
    end = time.time()
    timeperframe = (end-start)/N
    print("Average time per frame: {} s fps {}".format(timeperframe, 1/timeperframe))


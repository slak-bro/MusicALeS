import sys
from .screen import Screen
from multiprocessing import Process, Array as mpArray
import numpy as np
from arduino.driver.driver import Driver

class SerialDriverScreen(Screen):
    def __init__(self, nLeds):
        self.nLeds =nLeds
        self.driver = Driver()
        self.driver.setup(nLeds)
        
    def display(self, colorArray):
        assert len(colorArray) == self.nLeds
        self.driver.light(np.array(colorArray))

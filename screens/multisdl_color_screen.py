import sys
import sdl2.ext
from .screen import Screen
from multiprocessing import Process, Array as mpArray
import numpy as np

class MultiSDLColorScreen(Screen):
    def __init__(self, nLeds):
        self.nLeds =nLeds
        self.RESOURCES = sdl2.ext.Resources(__file__, "resources")
        sdl2.ext.init()
        self.SCREEN_HEIGHT = 200
        self.SCREEN_WIDTH = 840
        
        self.LED_WIDTH = self.SCREEN_WIDTH // self.nLeds
        self.renderProcess = None
        self.LEDS = [None, None]
        self.LEDS[0] = mpArray('i', [0,0,0]*self.nLeds)
        self.LEDS[1] = mpArray('i', [0,0,0]*self.nLeds)

        self.running = True
        self.renderProcess = Process(target=self._renderFunction)
        self.renderProcess.start()
        
    def display(self, colorArray, subscreen=0):
        assert len(colorArray) == self.nLeds
        flat = np.array(colorArray).flatten()
        for i in range(self.nLeds):
            self.LEDS[subscreen][3*i] = flat[3*i]
            self.LEDS[subscreen][3*i+1] = flat[3*i+1]
            self.LEDS[subscreen][3*i+2] = flat[3*i+2]

        
    def _renderFunction(self):
        self.window = sdl2.ext.Window("MultiColorScreen", size=(self.SCREEN_WIDTH,2*self.SCREEN_HEIGHT))
        self.windowsurface = self.window.get_surface()
        self.window.show()
        self.running = True
        while self.running:
            for i in range(self.nLeds):
                sdl2.ext.fill(self.windowsurface, 
                              sdl2.ext.Color(self.LEDS[0][3*i],self.LEDS[0][3*i+1],self.LEDS[0][3*i+2]), 
                              (i*self.LED_WIDTH,0,i*self.LED_WIDTH+100,self.SCREEN_HEIGHT))
                sdl2.ext.fill(self.windowsurface, 
                              sdl2.ext.Color(self.LEDS[1][3*i],self.LEDS[1][3*i+1],self.LEDS[1][3*i+2]), 
                              (i*self.LED_WIDTH,self.SCREEN_HEIGHT,i*self.LED_WIDTH+100,2*self.SCREEN_HEIGHT))
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    self.running = False
                    break
            self.window.refresh()
        return

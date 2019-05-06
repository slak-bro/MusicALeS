import sys
import sdl2.ext
from screens.screen import Screen
from multiprocessing import Process, Array as mpArray
import numpy as np

class SDLColorScreen(Screen):
    def __init__(self, nLeds):
        self.nLeds = nLeds
        self.RESOURCES = sdl2.ext.Resources(__file__, "resources")
        sdl2.ext.init()
        self.SCREEN_HEIGHT = 200
        self.SCREEN_WIDTH = 1530
        
        self.LED_WIDTH = self.SCREEN_WIDTH // self.nLeds
        self.renderProcess = None
        self.LEDS = mpArray('i', [0,0,0]*self.nLeds)

        self.running = True
        self.renderProcess = Process(target=self._renderFunction)
        self.renderProcess.start()
        
    def display(self, colorArray):
        assert len(colorArray) == self.nLeds
        flat = np.array(colorArray).flatten()
        for i in range(self.nLeds):
            self.LEDS[3*i] = flat[3*i]
            self.LEDS[3*i+1] = flat[3*i+1]
            self.LEDS[3*i+2] = flat[3*i+2]

        
    def _renderFunction(self):
        self.window = sdl2.ext.Window("SDL Color Screen", size=(self.SCREEN_WIDTH,self.SCREEN_HEIGHT), position=(0, 0))
        self.windowsurface = self.window.get_surface()
        self.window.show()
        self.running = True
        while self.running:
            for i in range(self.nLeds):
                sdl2.ext.fill(self.windowsurface, 
                              sdl2.ext.Color(self.LEDS[3*i],self.LEDS[3*i+1],self.LEDS[3*i+2]), 
                              (i*self.LED_WIDTH,0,i*self.LED_WIDTH+100,self.SCREEN_HEIGHT))
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    self.running = False
                    break
            self.window.refresh()
        return

if __name__ == "__main__":
    import time
    screen = SDLColorScreen(25)
    r,g,b = 0,0,0
    while True:
        screen.display([[(r+i)%255,(g+i)%255,(b+i)%255] for i in range(25)])
        time.sleep(0.03)
        r = (r+1)%255
        g = (g+1)%255
        b = (b+1)%255
    screen.renderProcess.join()
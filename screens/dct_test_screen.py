from .screen import Screen
from .sdl_color_screen import SDLColorScreen
from .multisdl_color_screen import MultiSDLColorScreen
import numpy as np
from scipy.fftpack import dct, idct
class DCTTestScreen(Screen):
    def __init__(self, nLeds, dctcomponents):
        self.nLeds = nLeds
        self.dctcomponent = dctcomponents
        #self.originalScreen = SDLColorScreen(nLeds, name="Original")
        self.screen = MultiSDLColorScreen(nLeds)

    def display(self, colorArray):
        self.screen.display(colorArray)
        a = np.array(colorArray)
        d = dct(np.transpose(a), norm="ortho")
        d[:,self.dctcomponent:].fill(0)
        a2 = idct(d, norm="ortho")
        a2 = np.transpose(a2)
        self.screen.display(a2.astype(int), 1)
    
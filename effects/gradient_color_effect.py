#!/usr/bin/python3

from effects.effect import Effect
from math import pi
import numpy as np
import random
import colorsys

HUE_ORANGE = 32
HUE_YELLOW = 64
HUE_GREEN = 96
HUE_AQUA = 128
HUE_BLUE = 160
HUE_PURPLE = 192
HUE_PINK = 224
HUES = [HUE_AQUA, HUE_BLUE, HUE_GREEN, HUE_ORANGE, HUE_PINK, HUE_PURPLE, HUE_YELLOW]
class GradientColorEffect(Effect):
    """
    Randomized color generator. 
    Simple. Basic.
    """

    def __init__(self, audio_source, screen, animator):
        super().__init__(audio_source, screen, animator)
        self.steps = 250
        hues = np.random.permutation(HUES)
        colors = [colorsys.hsv_to_rgb(h/255, 1, 1) for h in hues]
        self.colors_gradient = np.array([]).reshape(0,3)

        for i in range(len(hues)):
            j = (i+1)%len(hues)
            c = np.stack([
                np.linspace(colors[i][0], colors[j][0], self.steps), 
                np.linspace(colors[i][1], colors[j][1], self.steps), 
                np.linspace(colors[i][2], colors[j][2], self.steps)
            ], axis=1)
            self.colors_gradient = np.concatenate([self.colors_gradient, c])
        self.index = 0
        
    def get_color(self):
        c = self.colors_gradient[self.index]
        self.index = (self.index + 1) % len(self.colors_gradient)
        return c


    def apply_effect(self, data):
        """
        Find a color and apply it to the given input
        
        Args:
            data (list): input data - list of float or integers
        
        Returns:
            list: list of pixels that can directly be given to the screen
        """

        color = self.get_color()
        return np.array([x*color for x in data])

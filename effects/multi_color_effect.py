#!/usr/bin/python3

from effects.effect import Effect
from math import pi
import numpy as np
import random


class BasicColorEffect(Effect):
    """
    Randomized color generator. 
    Simple. Basic.
    """

    def __init__(self, audio_source, screen, animator):
        super().__init__(audio_source, screen, animator)
        self.color_loop_size = 250.
    
    def get_color(self):
        return np.array([0., 0.5, 0.5])

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

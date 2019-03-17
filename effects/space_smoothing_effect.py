#!/usr/bin/python3

from effects.effect import Effect

import numpy as np
from scipy.signal import savgol_filter


class SpaceSmoothingEffect(Effect):
    def __init__(self, window_length=7, polyorder=4, deriv=0, first_value=None, last_value=None):
        super().__init__()
        self.window_length = window_length
        self.polyorder = polyorder
        self.deriv = deriv
        self.first_value = first_value
        self.last_value = last_value
    
    def apply_effect(self, data):
        if self.first_value is not None:
            data[0] = self.first_value
        if self.last_value is not None:
            data[-1] = self.last_value
        processed_data = savgol_filter(data, self.window_length, self.polyorder, deriv=self.deriv)
        return np.clip([int(x) for x in processed_data], 0, 255)
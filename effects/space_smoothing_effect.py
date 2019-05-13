#!/usr/bin/python3

from effects.effect import Effect

import numpy as np
from scipy.signal import savgol_filter


class SpaceSmoothingEffect(Effect):
    def __init__(self, audio_source, screen, animator, window_length=7, polyorder=4, deriv=0, first_value=None, last_value=None):
        super().__init__(audio_source, screen, animator)
        self.window_length = window_length
        self.polyorder = polyorder
        self.deriv = deriv
        self.first_value = first_value
        self.last_value = last_value
    
    def apply_effect(self, data):
        #data = np.array(data).T
        #import ipdb; ipdb.set_trace()
        processed_data = savgol_filter(data, self.window_length, self.polyorder, deriv=self.deriv, mode="constant", axis=0)
        return np.clip(processed_data, 0, 255).astype(np.int32)
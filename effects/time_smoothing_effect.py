#!/usr/bin/python3

from effects.effect import Effect

import numpy as np
from scipy.signal import savgol_filter


class TimeSmoothingEffect(Effect):
    """
    Effect to smooth the leds colors modifications through time.
    An animator that uses this effect must have an attribute called 'history' that an instance of this effect will retrieve
    """

    def __init__(self, audio_source, screen, animator, history_ponderation=[0.1, 0.15, 0.25, 0.5]):
        super().__init__(audio_source, screen, animator)
        assert sum(history_ponderation) == 1., "Ponderation for TimeSmoothingEffect must have a sum equal to 1"
        self.history_ponderation = history_ponderation
        self.history_size = len(self.history_ponderation)
    
    def apply_effect(self, data):
        """
        Apply time smoothing effect on every dimension of the input array
        
        Args:
            data (list of lists): input data to apply effect on
        """

        history = np.array(self.animator.history + [data])
        result = [[0., 0., 0.] for _ in range(self.screen.nLeds)]

        for history_element, ponderation in zip(history, self.history_ponderation):
            result = np.add(result, ponderation*history_element)
        result = np.array([list(map(int, led)) for led in result])

        return result
#!/usr/bin/python3

from effects.effect import Effect

import numpy as np

class SymmetryEffect(Effect):
    def __init__(self, audio_source, screen, animator):
        super().__init__(audio_source, screen, animator)

    def apply_effect(self, data):
        return (data + np.flip(data, axis=0))//2
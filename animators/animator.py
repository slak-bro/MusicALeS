#!/usr/bin/python3

from abc import ABC, abstractmethod
import numpy as np


class Animator(ABC):
    def __init__(self, AudioSource, Screen):
        self.audio_source = AudioSource
        self.screen = Screen
    
    def start(self):
        self.audio_source.start()

    def prepare_for_leds(self, data):
        shape = data.shape
        data = data.flatten()
        for i in range(len(data)):
            data[i] = min(max(0, int(data[i])), 255)
        return np.reshape(data, shape).astype(np.int32)
    
    @abstractmethod
    def animate(self, data):
        """Animate the color screen; require a call to Animator.screen.display
        
        Args:
            data ([np float array]): sound data from the AudioSource
        """
        pass
    
    def zero(self):
        self.screen.zero()
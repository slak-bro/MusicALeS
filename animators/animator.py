#!/usr/bin/python3

from abc import ABC, abstractmethod

class Animator(ABC):
    def __init__(self, AudioSource, Screen):
        self.audio_source = AudioSource
        self.screen = Screen
    
    def start(self):
        self.audio_source.start()
    
    @abstractmethod
    def animate(self, data):
        """Animate the color screen; require a call to Animator.screen.display
        
        Args:
            data ([np float array]): sound data from the AudioSource
        """
        pass
    
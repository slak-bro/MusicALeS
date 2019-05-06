#!/usr/bin/python3

from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self, audio_source, screen, animator):
        self.audio_source = audio_source
        self.screen = screen
        self.animator = animator
    
    @abstractmethod
    def apply_effect(self, data):
        """
        Apply the effect on the given data
        
        Args:
            data (list): input data to apply effect on
        """

        pass

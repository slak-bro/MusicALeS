#!/usr/bin/python3

from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def apply_effect(self, data):
        """
        Apply the effect on the given data
        
        Args:
            data (list): input data to apply effect on
        """

        pass

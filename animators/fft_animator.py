#!/usr/bin/python3

from animators.animator import Animator
from effects.space_smoothing_effect import SpaceSmoothingEffect

from math import log
import numpy as np
from scipy.fftpack import fft

def grad(ca,cb,i,n):
    return [int((ca[k]+cb[k])*(i/n)) for k in range(3)]


class FFTAnimator(Animator):
    def __init__(self, audio_source, screen):
        super().__init__(audio_source, screen)
        self.sample_size = 2048
        self.audio_source.configure(44100, self.sample_size)
        self.audio_source.register_callback(self.animate)
        self.max = 0
        self.last_list = [[0]*3 for _ in range(self.screen.nLeds)]
        self.list_effects = [SpaceSmoothingEffect(first_value=0)]
    
    def smooth_value(self, data):
        return data
    
    def rescale_list(self, data):
        """
        Rescales the list in terms of size and return values between 0 and 255
        
        Args:
            data (list): list of calibrated data
        
        Returns:
            list: rescaled list
        """

        # Try to comment this line and you'll see what happen

        # Rescale the size of the list
        data = [data[int(i*(self.sample_size/self.screen.nLeds/2))] for i in range(self.screen.nLeds)]

        # Apply abs function and get a color value
        data = list(map(abs, data))
        self.max = max(data)
        return [int(255*x/self.max) for x in data[:self.screen.nLeds]]
    
    def calibrate(self, y):
        """
        Calibrates the data list using a simple square function. This is designed so that the bass takes more room on the screen than
        if the absciss was linear
        
        Args:
            y ([type]): [description]
        
        Returns:
            [type]: [description]
        """

        # If the first value is not set to zero, the end result is pretty bad (even with SpaceSmoothingEffect)
        y[0] = 0
        return [y[int(i**2 / self.sample_size)] for i in range(self.sample_size)]  # here self.sample_size == len(y)
    
    def apply_effects(self, values):
        for effect in self.list_effects:
            values = effect.apply_effect(values)
        return values

    def apply_color(self, values):
        return [[x, 0, x] for x in values]
    
    def animate(self, data):
        cal_Y = fft(data)[:self.sample_size]
        
        try:
            cal_Y = self.calibrate(cal_Y)
            cal_Y = self.rescale_list(cal_Y)
        except ValueError:
            self.screen.display(self.last_list)
            return

        cal_Y = self.apply_effects(cal_Y)
        cal_Y = self.apply_color(cal_Y)
        self.last_list = self.smooth_value(cal_Y)
        self.screen.display(self.last_list)

#!/usr/bin/python3

from animators.animator import Animator
from effects.basic_color_effect import BasicColorEffect
from effects.space_smoothing_effect import SpaceSmoothingEffect
from effects.time_smoothing_effect import TimeSmoothingEffect
from effects.symmetry_effect import SymmetryEffect

from math import log
import numpy as np
from scipy.fftpack import fft

def grad(ca,cb,i,n):
    return [int((ca[k]+cb[k])*(i/n)) for k in range(3)]


class FFTAnimator(Animator):

    name = "fft"

    def __init__(self, audio_source, screen):
        super().__init__(audio_source, screen)
        self.sample_size = 2048
        self.kept_fft_values = int(self.sample_size/2)
        self.audio_source.configure(44100, self.sample_size)
        self.audio_source.register_callback(self.animate)
        self.max = 0
        self.history_ponderation =  [0.1, 0.2, 0.3, 0.4]
        self.history = np.array([[[0, 0, 0] for _ in range(self.screen.nLeds)]] * (len(self.history_ponderation) - 1))

        self.effect_args = [self.audio_source, self.screen, self]
        # List of effects. Order matters!
        self.list_effects = [SpaceSmoothingEffect(*self.effect_args, first_value=[0, 0, 0]),
                             TimeSmoothingEffect(*self.effect_args, history_ponderation=self.history_ponderation),
                             BasicColorEffect(*self.effect_args),
                             SymmetryEffect(*self.effect_args),]
    
    def rescale_list(self, data):
        """
        Rescales the list in terms of size and return values between 0 and 255
        
        Args:
            data (list): list of calibrated data
        
        Returns:
            list: rescaled list
        """


        # Rescale the size of the list
        data = [data[int(i*(self.kept_fft_values/self.screen.nLeds))] for i in range(self.screen.nLeds)]

        # Apply abs function and get a color value
        data = list(map(abs, data))
        self.max = max(data)
        return [[int(255*x/self.max)] for x in data[:self.screen.nLeds]]
    
    def calibrate(self, y):
        """
        Calibrates the data list using a simple square function. This is designed so that the bass takes more room on the screen than
        if the absciss was linear
        
        Args:
            y (list): input list to calibrate
        
        Returns:
            list: calibrated list
        """

        # If the first value is not set to zero, the end result is pretty bad (even with SpaceSmoothingEffect)
        y[0] = 0

        return [y[int(i**2 / self.kept_fft_values)] for i in range(self.kept_fft_values)]  # here self.sample_size == len(y)
    
    def apply_effects(self, values):
        for effect in self.list_effects:
            values = effect.apply_effect(values)
        return values
    
    def animate(self, data):
        cal_Y = fft(data)[:self.kept_fft_values]
        try:
            cal_Y = self.calibrate(cal_Y)
            cal_Y = self.rescale_list(cal_Y)
        except ValueError:
            self.screen.display(self.history[-1])
            return

        cal_Y = self.apply_effects(cal_Y)
        cal_Y = self.prepare_for_leds(cal_Y)

        self.history = np.append(self.history[1:], [cal_Y], axis=0)
        
        self.screen.display(cal_Y)

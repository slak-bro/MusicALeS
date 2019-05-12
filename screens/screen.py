from abc import ABC, abstractmethod

import numpy as np
from utils.rgb_to_hsv_np import rgb_to_hsv, hsv_to_rgb

class Screen(ABC):
    @abstractmethod
    def display(self, colorArray):
        """Display colorArray (length Screen.nLeds) on the screen
        
        Args:
            colorArray ([R,G,B]*nLeds): R,G,B between 0 and 255
        """
        pass

    def apply_brightness(self, colorArray):
        """Apply brightness modification to the colors

        Args:
            colorArray (ndarray): input array

        Returns:
            ndarray: output array with colors modified with brightness
        """
        hsv = rgb_to_hsv(colorArray)
        hsv[:,2] *= self.brightness
        rgb = hsv_to_rgb(hsv)
        return rgb.astype(np.int32)

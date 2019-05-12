from abc import ABC, abstractmethod

from colorsys import rgb_to_hsv, hsv_to_rgb

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

        for led_index in range(self.nLeds):
            hsv_color = list(rgb_to_hsv(*colorArray[led_index]))
            hsv_color[2] *= self.brightness
            colorArray[led_index] = [int(x) for x in hsv_to_rgb(*hsv_color)]
        return colorArray

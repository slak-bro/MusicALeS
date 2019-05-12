from abc import ABC, abstractmethod

class Screen(ABC):
    @abstractmethod
    def display(self, colorArray):
        """Display colorArray (length Screen.nLeds) on the screen
        
        Args:
            colorArray ([R,G,B]*nLeds): R,G,B between 0 and 255
        """
        pass

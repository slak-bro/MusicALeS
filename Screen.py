from abc import ABC, abstractmethod

class Screen(ABC):
    @abstractmethod
    def display(self, colorArray):
        pass
    
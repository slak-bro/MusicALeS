from abc import ABC, abstractmethod

class AudioSource(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def configure(self, sample_rate, buffer_size):
        """Configure the sound callback properties
        
        Args:
            sample_rate ([int]): sample per seconds (Hz)
            buffer_size ([int]): number of sample per callback call
        """

        pass

    @abstractmethod
    def register_callback(self, callback):
        """Register the audio callback
        
        Args:
            callback (function(data)): function to call with self.buffer_size samples
        """
        pass
    
    @abstractmethod
    def start(self):
        """Start the audio source processing
        """

        pass
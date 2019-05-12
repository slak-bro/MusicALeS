from .audio_source import AudioSource
import numpy as np
import sounddevice as sd

class SoundDeviceAudioSource(AudioSource):
    """
    Audio source using python's sounddevice library
    """
    name = "sounddevice"
    def __init__(self, device):
        self.device = device
        self.callback = None
    def configure(self, sample_rate, buffer_size):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        
    def register_callback(self, callback):
        self.callback = callback

    def start(self):
        assert self.callback is not None
        future_data = sd.rec(self.buffer_size, samplerate=self.sample_rate, channels=1, device=self.device)
        while True:
            sd.wait()
            data = future_data
            future_data = sd.rec(self.buffer_size, samplerate=self.sample_rate, channels=1, device=self.device)
            self.callback(data)

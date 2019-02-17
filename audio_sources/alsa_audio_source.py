from .audio_source import AudioSource
import numpy as np
import struct
import time
import alsaaudio
from multiprocessing import Process


class ALSAAudioSource(AudioSource):
    """ALSA Capture device AudioSource
    Initialise loopback device
        $ modprobe snd-aloop
    Allow pulseaudio loopback listening
        $ pactl load-module module-loopback
    Tweak audio routing
        $ pavucontrol
    Args:
        AudioSource ([type]): [description]
    """

    def __init__(self):
        self.sink = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device="hw:CARD=Loopback,DEV=1")
        self.callback = None
    
    def configure(self, sample_rate, buffer_size):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        self.buffer_split = 1

        self.sink.setchannels(1)
        self.sink.setformat(alsaaudio.PCM_FORMAT_S32_LE)
        self.sink.setrate(self.sample_rate)
        self.sink.setperiodsize(self.buffer_size)
        
    def register_callback(self, callback):
        self.callback = callback

    def start(self):
        assert self.callback is not None
        while True:
            try:
                data = None
                for _ in range(self.buffer_split):
                    _, tdata = self.sink.read()
                    tdata = np.array(list(struct.iter_unpack("<i", tdata)), dtype=np.float32)
                    data = tdata if data is None else np.concatenate([data, tdata])
                data = data.flatten()
                self.callback(data)
            except alsaaudio.ALSAAudioError:
                print("Trying to split alsa buffer size ... new splitted buffer_size:{}".format(self.buffer_size//2))
                self.buffer_size //= 2
                self.sink.setperiodsize(self.buffer_size)
                self.buffer_split *= 2

if __name__ == "__main__":
    def mycb(data):
        print(len(data), np.average(data))
    aas = ALSAAudioSource()
    aas.configure(44100, 5000)
    aas.register_callback(mycb)
    aas.start()
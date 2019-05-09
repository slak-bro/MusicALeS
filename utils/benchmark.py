"""
Handle animators benchmarking by creating a dummy audio source calling the animate method
"""
import numpy as np
import cProfile, pstats
import sys
import time

from screens.screen import Screen
class DummyScreen(Screen):
    def __init__(self, nLeds):
        self.nLeds = nLeds
    def display(self, colorArray):
        return

from audio_sources.audio_source import AudioSource
class DummyAudioSource(AudioSource):
    def __init__(self, npass):
        self.callback = None
        self.npass = npass
    def configure(self, sample_rate, buffer_size):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
    def register_callback(self, callback):
        self.callback = callback
    def start(self):
        data = np.random.rand(self.npass, self.buffer_size)
        pr = cProfile.Profile()
        start = time.time()
        pr.enable()
        for i in range(self.npass):
            self.callback(data[i])
        pr.disable()
        end = time.time()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=sys.stdout).sort_stats(sortby)
        print("Average time per animation call: {:6.2f} ms".format((end-start)*1000/self.npass))
        ps.print_stats()

def benchmark(Animator, npass, nLeds = 300):
    """
    Benchmark the animator and print bench infos
    
    Args:
        Animator: the animator class to benchmark
        npass: number of test pass to perform
        nLeds: number of leds to simulate
    """
    
    audio_source = DummyAudioSource(npass)
    screen = DummyScreen(nLeds)
    Animator(audio_source, screen).start()

    

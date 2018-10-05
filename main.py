import alsaaudio, time, audioop
import numpy as np
import random
import scipy.io.wavfile, scipy
import struct
import sys

from beat_detector import BeatDetector
from color_screen import ColorScreen


batch_size = 10  # in ms

if __name__ == "__main__":

    color_screen_list = [ColorScreen(0., 200.)]
    beat_detector = BeatDetector(240, 4096, color_screen_list)
    beat_detector.listen()

    #wav = np.array(wav, dtype=np.int16)
    #scipy.io.wavfile.write("lul.wav", rate=44100, data=wav)

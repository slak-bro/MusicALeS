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

    color_screen_list = [ColorScreen("Low", 0., 85., [50., 100.]), ColorScreen("Mid", 250., 1000., [200., 400.])]
    beat_detector = BeatDetector(44100, 44032, 256, ColorScreen("Low", 0., 8000., []))
    beat_detector.listen(20)

    for cs in color_screen_list:
        cs.plot_pitches()
        cs.write_signal()

    #wav = np.array(wav, dtype=np.int16)
    #scipy.io.wavfile.write("lul.wav", rate=44100, data=wav)

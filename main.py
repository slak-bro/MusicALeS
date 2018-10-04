import random
import sys

from beat_detector import BeatDetector
from color_screen import ColorScreen


batch_size = 10  # in ms

if __name__ == "__main__":
    filename = sys.argv[1]
    beat_detector = BeatDetector(filename, batch_size)
    #beats_list = beat_detector.get_beats_list()

    color_screen = ColorScreen(100, [[random.random()]*3]*100)
    color_screen.animate()

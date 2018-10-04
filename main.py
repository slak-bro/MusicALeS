import sys

from beat_detector import BeatDetector

if __name__ == "__main__":
    filename = sys.argv[1]
    beat_detector = BeatDetector(filename)
    beats_list = beat_detector.get_beats_list()

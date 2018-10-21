import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy_ringbuffer import RingBuffer
import random
import scipy.io.wavfile
import time
import colorsys

colors_list = [[int(random.random()*255) for _ in range(3)] for _ in range(100)]

class ColorScreen(object):

    def __init__(self, name, MIN_PITCH, MAX_PITCH, rescale_range, smoothing=50):
        self.name = name
        self.MIN_PITCH = MIN_PITCH
        self.MAX_PITCH = MAX_PITCH
        self.min_pitch_range = float('inf')
        self.max_pitch_range = float('-inf')
        self.rescale_range = rescale_range
        self.img = np.zeros((512,512,3), np.uint8)
        self.smooth_buffer = RingBuffer(capacity=smoothing, dtype=np.int)
        self.all_pitches = []
        self.full_signal = []

    def pitch_to_color(self, pitch):
        scaled_pitch = self.scale_pitch(pitch)
        # scaled_pitch = (pitch - self.min_pitch_range) / (self.max_pitch_range - self.min_pitch_range)
        color = colorsys.hsv_to_rgb(scaled_pitch,0.5,0.5)
        color = tuple([int(e*255) for e in color])
        return color

    def scale_pitch(self, pitch):
        while pitch < self.rescale_range[0]:
            pitch *= 2
            print(pitch)
        while pitch > self.rescale_range[1]:
            pitch /= 2
            print(pitch)
        self.all_pitches.append(pitch)
        return pitch

    def animate(self, beat):
        """Animates the color screen
        
        Arguments:
            beat {float} -- beat index compared to local average
        """

        print(beat)
        #self.smooth_buffer.append(beat)
        color = self.beat_to_color(beat)
        cv2.rectangle(self.img, (0,0), (511,511), color, 1000)
        cv2.imshow(self.name, self.img)
        cv2.waitKey(10)

    def beat_to_color(self, beat):
        """
        transforms a beat index to a colro
        
        Arguments:
            beat {float} -- beat index
        
        Returns:
            tuple -- RGB color tuple
        """

        # color = colorsys.hsv_to_rgb(min(1, beat/5),0.5,0.5)
        # color = tuple([int(e*255) for e in color])
        color = tuple([beat*20 for _ in range(3)])
        return color

    def finish():
        cv2.destroyAllWindows()

    def plot_pitches(self):
        plt.plot(np.arange(len(self.all_pitches)), self.all_pitches)
        plt.show()

    def write_signal(self):
        # import ipdb; ipdb.set_trace()
        self.full_signal = np.array(self.full_signal, dtype=np.float32)
        scipy.io.wavfile.write(str(self.MIN_PITCH)+".wav", 22050, self.full_signal)
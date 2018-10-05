import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy_ringbuffer import RingBuffer
import random
import time
import colorsys

colors_list = [[int(random.random()*255) for _ in range(3)] for _ in range(100)]

class ColorScreen(object):

    def __init__(self, name, MIN_PITCH, MAX_PITCH, smoothing=10):
        self.name = name
        self.MIN_PITCH = MIN_PITCH
        self.MAX_PITCH = MAX_PITCH
        self.min_pitch_range = float('inf')
        self.max_pitch_range = float('-inf')
        self.img = np.zeros((512,512,3), np.uint8)
        self.smooth_buffer = RingBuffer(capacity=smoothing, dtype=np.int)

    def pitch_to_color(self, pitch):
        if self.min_pitch_range == self.max_pitch_range:
            return (0, 0, 0)
        #import ipdb; ipdb.set_trace()
        scaled_pitch = (pitch - self.min_pitch_range) / (self.max_pitch_range - self.min_pitch_range)
        color = colorsys.hsv_to_rgb(scaled_pitch,0.5,0.5)
        color = tuple([int(e*255) for e in color])
        return color

    def animate(self, pitch):
        if pitch == 0.0:
            return
        print(pitch)
        self.min_pitch_range = min(self.min_pitch_range, pitch)
        self.max_pitch_range = max(self.max_pitch_range, pitch)
        self.smooth_buffer.append(pitch)
        avg_pitch = np.average(self.smooth_buffer) - 48
        color = self.pitch_to_color(avg_pitch)
        cv2.rectangle(self.img, (0,0), (511,511), color, 1000)
        cv2.imshow(self.name, self.img)
        cv2.waitKey(10)

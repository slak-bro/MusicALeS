#!/usr/bin/python3

from effects.effect import Effect
from math import pi
import numpy as np
import random


ORANGE = (1., 0.27, 0.)
YELLOW = (1., 1., 0.)
GREEN = (0., 1., 0.)
AQUA = (0., 1., 1.)
BLUE = (0., 0., 1.)
PURPLE = (1., 0., 1.)
COLORS = [ORANGE, YELLOW, GREEN, AQUA, BLUE, PURPLE]


def grad(v,n):
    a = np.linspace(0,v,n)
    return np.transpose(np.array([a, np.zeros([n]), a], dtype=np.uint8))

class MultiColorEffect(Effect):
    """
    Randomized color generator. 
    Simple. Basic.
    """

    def __init__(self, audio_source, screen, animator):
        super().__init__(audio_source, screen, animator)
        self.color_loop_size = 50
        self.index = 0

        self.current_left_color = random.choice(COLORS)
        self.next_left_color = self.current_left_color
        while self.next_left_color == self.current_left_color:
            self.next_left_color = random.choice(COLORS)

        self.current_right_color = random.choice(COLORS)
        self.next_right_color = self.current_right_color
        while self.current_right_color == self.next_right_color:
            self.next_right_color = random.choice(COLORS)
        print("cur", self.current_left_color, self.current_right_color)
        print("next", self.next_left_color, self.next_right_color)

    def get_side_color(self, side):
        if self.index % self.color_loop_size == 0:
            self.index = 0
            # Choose the next color to gradient towards
            current_color = self.next_left_color if side == "left" else self.next_right_color
            new_color = current_color
            while new_color == current_color:
                new_color = random.choice(COLORS)
            print(new_color)
            # Affect new colors and return the right one
            if side == "left":
                self.current_left_color = current_color
                self.next_left_color = new_color
                return self.current_left_color
            else:
                self.current_right_color = current_color
                self.next_right_color = new_color
                return self.current_right_color
        else:
            if side == "left":
                return tuple([x + (y-x)/self.color_loop_size*self.index for x,y in zip(self.current_left_color, self.next_left_color)])
            if side == "right":
                return tuple([x + (y-x)/self.color_loop_size*self.index for x,y in zip(self.current_right_color, self.next_right_color)])
    
    def get_colors(self, amount):
        """
        Returns an array of colors to be displayed on the led strip

        Args:
            amount (int): amount of colors to compute (=amount of leds on the strip)

        Returns:
            np.array: array of colors, shape (amount,3)
        """

        left_color = self.get_side_color("left")
        right_color = self.get_side_color("right")
        #print(left_color, right_color)
        reds = np.linspace(left_color[0], right_color[0], amount)
        greens = np.linspace(left_color[1], right_color[1], amount)
        blues = np.linspace(left_color[2], right_color[2], amount)
        #print(np.transpose(np.array([reds, greens, blues])))
        return np.transpose(np.array([reds, greens, blues]))

    def apply_effect(self, data):
        """
        Find a color and apply it to the given input
        
        Args:
            data (list): input data - list of float or integers
        
        Returns:
            list: list of pixels that can directly be given to the screen
        """

        self.index += 1
        colors = self.get_colors(amount=len(data))
        return np.array([x * color for x,color in zip(data, colors)])

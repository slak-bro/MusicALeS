#!/usr/bin/python3

from animators.animator import Animator
import numpy as np

import time
def grad(v,n):
    a = np.linspace(0,v,n)
    return np.transpose(np.array([a, np.zeros([n]), a], dtype=np.uint8)

class EnergyAnimator(Animator):
    def __init__(self, audio_source, screen):
        super().__init__(audio_source, screen)
        self.audio_source.configure(22000, 400)
        self.audio_source.register_callback(self.animate)
        self.val = 255
        self.buffer = [0 for _ in range(20)]
        self.last_value = 0.

    def smooth_value(self, value):
        result = max(value, self.last_value - 5)
        self.last_value = int(result)
        return int(result)

    def animate(self, data):
        energy = np.sum(np.square(data))
        max_val = max(energy, max(self.buffer))
        self.buffer = self.buffer[1:] + [energy]
        v = self.smooth_value(int(155 * energy / max_val) if max_val > 0 else 0)
        self.screen.display(grad(v,self.screen.nLeds))

if __name__ == "__main__":
    from audio_sources.file_audio_source import FileAudioSource
    #from audio_sources.alsa_audio_source import ALSAAudioSource
    from screens.sdl_color_screen import SDLColorScreen
    audio_source = FileAudioSource("traindata/skeler-in_my_mind.mp3")
    #audio_source = ALSAAudioSource()
    screen = SDLColorScreen(50)
    animator = EnergyAnimator(audio_source, screen)
    animator.start()
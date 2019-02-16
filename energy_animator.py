from animator import Animator
import numpy as np
class EnergyAnimator(Animator):
    def __init__(self, audio_source, screen):
        super().__init__(audio_source, screen)
        self.audio_source.configure(44100, 44100//10)
        self.audio_source.register_callback(self.animate)
        self.val = 255
        self.max = 0
    def animate(self, data):
        energy = np.sum(np.square(data))
        self.max = max(energy, self.max)
        v = int(153 * energy /self.max)
        self.screen.display([[v,0,v] for i in range(self.screen.nLeds)])
        


if __name__ == "__main__":
    from file_audio_source import FileAudioSource
    from SDL_color_screen import SDLColorScreen
    audio_source = FileAudioSource("traindata/cvrl-subterfuge.mp3")
    screen = SDLColorScreen(50)
    animator = EnergyAnimator(audio_source, screen)
    animator.start()
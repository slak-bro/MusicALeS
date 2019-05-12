from animators.animator import Animator
import numpy as np
from scipy.signal import butter, lfilter, freqz


def grad(ca,cb,i,n):
    return [int((ca[k]+cb[k])*(i/n)) for k in range(3)]


class BassEnergyAnimator(Animator):

    name = "bass_energy"

    def __init__(self, audio_source, screen):
        super().__init__(audio_source, screen)
        self.sample_rate = 16000
        self.audio_source.configure(self.sample_rate, self.sample_rate//30)
        self.audio_source.register_callback(self.animate)
        self.val = 255
        self.buffer = [0 for _ in range(20)]
        self.last_value = 0.
        self.cutoff = 55
        self.filter_order = 6
        self.b, self.a = self.butter_lowpass()
    
    def butter_lowpass_filter(self, data):
        y = lfilter(self.b, self.a, data)
        return y

    def butter_lowpass(self):
        nyq = 0.5 * self.sample_rate
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.filter_order, normal_cutoff, btype='low', analog=False)
        return b, a

    def smooth_value(self, value):
        result = max(value, self.last_value - 5)
        self.last_value = int(result)
        return int(result)

    def animate(self, data):
        filtered_data = self.butter_lowpass_filter(data)
        energy = np.sum(np.square(filtered_data))
        max_val = max(energy, max(self.buffer))
        self.buffer = self.buffer[1:] + [energy]
        v = self.smooth_value(int(155 * energy / max_val) if max_val > 0 else 0)
        self.screen.display([grad([v,0,v],[0,0,0],i,self.screen.nLeds) for i in range(self.screen.nLeds)])


if __name__ == "__main__":
    from audio_sources.file_audio_source import FileAudioSource
    #from audio_sources.alsa_audio_source import ALSAAudioSource    
    from screens.sdl_color_screen import SDLColorScreen
    audio_source = FileAudioSource("traindata/skeler-in_my_mind.mp3")
    #audio_source = ALSAAudioSource()
    screen = SDLColorScreen(50)
    animator = BassEnergyAnimator(audio_source, screen)
    animator.start()
from .audio_source import AudioSource
from pydub import AudioSegment
from pydub.utils import get_array_type
import array
import numpy as np
import time
from multiprocessing import Process
from pydub.playback import play


class FileAudioSource(AudioSource):
    def __init__(self, path):
        self.sound = AudioSegment.from_file(file=path)
        self.callback = None
    
    def configure(self, sample_rate, buffer_size):
        self.mono = self.sound.split_to_mono()[0]
        self.sample_rate = sample_rate
        self.mono = self.mono.set_frame_rate(sample_rate)
        self.buffer_size = buffer_size
        bit_depth = self.mono.sample_width * 8
        array_type = get_array_type(bit_depth)
        self.numeric_array = np.array(array.array(array_type, self.mono._data))

    def register_callback(self, callback):
        self.callback = callback

    def start(self):
        assert self.callback is not None
        self.play_process = Process(target=play, args=(self.sound,))
        self.start_time = time.time()
        self.play_process.start()
        song_duration = len(self.sound)
        previous_frameIndex = -self.buffer_size
        play_time = time.time() - self.start_time
        while play_time < song_duration:
            frameIndex = int(play_time * self.sample_rate)
            if frameIndex > self.buffer_size and frameIndex - previous_frameIndex >= self.buffer_size:
                data = self.numeric_array[frameIndex-self.buffer_size: frameIndex]
                data = np.array(data, dtype=np.float)
                self.callback(data)
                previous_frameIndex = frameIndex
            play_time = time.time() - self.start_time
        self.play_process.terminate()

if __name__ == "__main__":
    def mycb(data):
        print(data[:20])
    fas = FileAudioSource("traindata/cvrl-subterfuge.mp3")
    fas.configure(44100, 4000)
    fas.register_callback(mycb)
    fas.start()
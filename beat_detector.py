import alsaaudio, aubio, audioop
import pydub
import numpy as np
import scipy.io.wavfile
import struct


class BeatDetector(object):

    def __init__(self, time_in_sec, sample_size, color_screen_list):
        self.time_in_sec = time_in_sec
        self.color_screen = color_screen_list[0]
        self.sample_size = sample_size
        self.mini_batches = int(self.sample_size / 1024)

    def listen(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        inp.setchannels(1)
        inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        inp.setperiodsize(1024)

        wav = []

        for _ in range(int(self.time_in_sec * 44100 / self.sample_size)):
            wav = []
            for _ in range(self.mini_batches):
                l, data = inp.read()
                data = list(struct.iter_unpack("<f", data))
                wav += data
            wav = np.array(wav, dtype=np.float32)[:,0]
            pitch = self._process_pitch(wav)
            self.color_screen.animate(pitch)


    def _load_data(self):
        """
        load data from file self.filename
        :return:
        """

        mp3_file = pydub.AudioSegment.from_mp3(self.filename + ".mp3")
        mp3_file.export(self.filename + ".wav", format="wav")
        self.rate, data = scipy.io.wavfile.read(self.filename + ".wav")
        self.signal = data[:,0] / 2 + data[:,1] / 2

    def _process_pitch(self, data):
        pitch_detector = aubio.pitch("default", self.sample_size*2, self.sample_size, 44100)
        pitch_detector.set_unit("Hz")
        pitch = pitch_detector(data)[0]
        return int(pitch)

    def get_pitch_list(self):
        self._load_data()
        pitch = self._process_pitch()

    def _process_beats(self):
        pass

    def get_beats_list(self):
        self._load_data()
        self._process_beats()

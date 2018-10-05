import alsaaudio, aubio, audioop
import pydub
import numpy as np
import scipy.io.wavfile
from scipy.signal import butter, lfilter, freqz
import struct

order = 5
fs = 22050


def butter_bandpass(lowcut, highcut):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut):
    b, a = butter_bandpass(lowcut, highcut)
    y = np.array(lfilter(b, a, data), dtype=np.float32)
    return y

def butter_lowpass(cutoff):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff):
    b, a = butter_lowpass(cutoff)
    y = np.array(lfilter(b, a, data), dtype=np.float32)
    return y


class BeatDetector(object):

    def __init__(self, time_in_sec, sample_size, color_screen_list):
        self.time_in_sec = time_in_sec
        self.color_screen_list = color_screen_list
        self.sample_size = sample_size
        self.mini_batches = int(self.sample_size / 1024)

    def listen(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        inp.setchannels(1)
        inp.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        inp.setperiodsize(1024)

        wav = []

        for _ in range(int(self.time_in_sec * fs / self.sample_size)):
            wav = []
            for _ in range(self.mini_batches):
                l, data = inp.read()
                data = list(struct.iter_unpack("<f", data))
                wav += data
            wav = np.array(wav, dtype=np.float32)[:,0]

            pitches = []
            for screen in self.color_screen_list:
                #print(max(wav), min(wav))
                pitch = self._process_pitch(wav, screen)
                pitches.append(pitch)
                if not pitch:
                    continue
                screen.animate(pitch)
            if max(pitches) != 0:
                print(pitches)

    def _load_data(self):
        """
        load data from file self.filename
        :return:
        """

        mp3_file = pydub.AudioSegment.from_mp3(self.filename + ".mp3")
        mp3_file.export(self.filename + ".wav", format="wav")
        self.rate, data = scipy.io.wavfile.read(self.filename + ".wav")
        self.signal = data[:,0] / 2 + data[:,1] / 2

    def _process_pitch(self, data, screen):
        low, high = screen.MIN_PITCH, screen.MAX_PITCH
        if not low:
            filtered_data = butter_lowpass_filter(data, high)
        else:
            filtered_data = butter_bandpass_filter(data, low, high)
        #import ipdb; ipdb.set_trace()
        screen.full_signal += filtered_data.tolist()
        pitch_detector = aubio.pitch("default", self.sample_size*2, self.sample_size, 44100)
        pitch_detector.set_unit("Hz")
        pitch = pitch_detector(filtered_data)[0]
        return int(pitch)

    def get_pitch_list(self):
        self._load_data()
        pitch = self._process_pitch()

    def _process_beats(self):
        pass

    def get_beats_list(self):
        self._load_data()
        self._process_beats()

import pydub
import scipy.io.wavfile


class BeatDetector(object):

    def __init__(self, filename, batch_size):
        self.filename = filename
        self.batch_size = batch_size  # in ms

        # filled during process
        self.rate = None
        self.signal = None

    def _load_data(self):
        """
        load data from file self.filename
        :return:
        """

        mp3_file = pydub.AudioSegment.from_mp3(self.filename + ".mp3")
        mp3_file.export(self.filename + ".wav", format="wav")
        self.rate, data = scipy.io.wavfile.read(self.filename + ".wav")
        self.signal = data[:,0] / 2 + data[:,1] / 2

    def _process_pitch(self):
        pass

    def get_pitch_list(self):
        self._load_data()
        self._process_pitch()

    def _process_beats(self):
        pass

    def get_beats_list(self):
        self._load_data()
        self._process_beats()

import pydub
import scipy.io.wavfile

class BeatDetector(object):

    def __init__(self, filename):
        self.filename = filename

        # filled during process
        self.rate = None
        self.signal = None

    def load_data(self):
        """
        load data from file self.filename
        :return:
        """

        mp3_file = pydub.AudioSegment.from_mp3(self.filename + ".mp3")
        mp3_file.export(self.filename + ".wav", format="wav")
        self.rate, data = scipy.io.wavfile.read(self.filename + ".wav")
        self.signal = data[:,0] / 2 + data[:,1] / 2

    def process(self):
        pass

    def get_beats_list(self):
        self.load_data()

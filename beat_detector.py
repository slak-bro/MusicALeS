import pydub
import scipy.io.wavfile

class BeatDetector(object):

    def __init__(self, filename):
        self.filename = filename

        # filled during process
        self.rate = -1

    def load_data(self):
        """
        load data from file self.filename
        :return:
        """

        mp3_file = pydub.AudioSegment.from_mp3(self.filename + ".mp3")
        mp3_file.export(self.filename + ".wav", format="wav")
        self.rate, audData = scipy.io.wavfile.read(self.filename + ".wav")
        self.signal = (audData[:,0] + audData[:,1]) / 2
        print(max(self.signal))
        import ipdb; ipdb.set_trace()

        print(self.rate)
        print(audData.shape)

    def process(self):
        pass

    def get_beats_list(self):
        self.load_data()
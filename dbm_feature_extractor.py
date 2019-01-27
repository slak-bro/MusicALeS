import array
from pydub import AudioSegment
from pydub.utils import get_array_type, mediainfo
import numpy as np
from functools import partial
SAMPLE_RATE = 22050 
NSAMPLES = 1024 # Number of sample for each feature extraction step

def mp3preprocess(path):
    sound = AudioSegment.from_file(file=path)
    mono = sound.split_to_mono()[0] # TODO maybe concat both sides to have more mono data
    mono = mono.set_frame_rate(SAMPLE_RATE)
    bit_depth = mono.sample_width * 8
    array_type = get_array_type(bit_depth)
    numeric_array = np.array(array.array(array_type, mono._data))
    numeric_array = numeric_array[:-(len(numeric_array)%NSAMPLES)]
    frames = np.array_split(numeric_array, len(numeric_array)/NSAMPLES)
    frames = map(partial(np.fft.fft, n=NSAMPLES//2 +1, norm="ortho"), frames)
    frames = map(np.absolute, frames)
    return np.array(list(frames))
    


from dbn.tensorflow import UnsupervisedDBN
class DBNFeatureExtractor(object):
    def __init__(self):
        self.dbn = UnsupervisedDBN(hidden_layers_structure=[513, 50, 50, 50],
                                   batch_size=100,
                                   learning_rate_rbm=0.001,
                                   n_epochs_rbm=5,
                                   activation_function='sigmoid')
    def train(self, frames):
        self.dbn.fit(frames)
    def extractFeatures(self, parameter_list):
        pass

if __name__ == "__main__":
    dbn = DBNFeatureExtractor()
    train_data = mp3preprocess("traindata/cvrl-subterfuge.mp3")
    print(train_data.shape)
    dbn.train(train_data)
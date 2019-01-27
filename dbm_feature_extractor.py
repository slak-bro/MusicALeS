import array
from pydub import AudioSegment
from pydub.utils import get_array_type, mediainfo
import numpy as np
from functools import partial
import sys, os
from multiprocessing import Pool

SAMPLE_RATE = 22050 
NSAMPLES = 1024 # Number of sample for each feature extraction step

def mp3preprocess(path):
    print(path)
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
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt

class DBNFeatureExtractor(object):
    def __init__(self, load=False):
        if load:
            self.dbn = UnsupervisedDBN.load("dbn.pickle")
            self.pca = pickle.load(open("pca.pickle", "rb"))
        else:
            self.dbn = UnsupervisedDBN(hidden_layers_structure=[513, 50, 50, 50],
                                       batch_size=700,
                                       learning_rate_rbm=0.001,
                                       n_epochs_rbm=5,
                                       activation_function='sigmoid')
            self.pca = PCA(n_components=2)
    def save(self):
        self.dbn.save("dbn.pickle")
        pickle.dump(self.pca, open("pca.pickle", "wb"))

    def train(self, frames):
        self.dbn.fit(frames)
        raw_features = self.dbn.transform(frames)
        self.pca.fit(raw_features)
        plt.figure(1, figsize=(4, 3))
        plt.clf()
        plt.axes([.2, .2, .7, .7])
        plt.plot(self.pca.explained_variance_, linewidth=2)
        plt.axis('tight')
        plt.xlabel('n_components')
        plt.ylabel('explained_variance_')
        plt.show()

    def extractFeatures(self, frame):
        raw_features = self.dbn.transform(frame)
        return self.pca.transform(raw_features)

if __name__ == "__main__":
    TRAIN_DATA_PATH = "./traindata"
    dbn = None
    if sys.argv[1] == "train":
        paths = []
        for root, dirs, files in os.walk(TRAIN_DATA_PATH):  
            for filename in files:
                if filename[-4:] == ".mp3":
                    paths.append(TRAIN_DATA_PATH+"/"+filename)
        p = Pool(8)
        train_data = p.map(mp3preprocess, paths)
        print("Data preprocessing done")
        train_data = np.concatenate(np.array(train_data))
        print(train_data.shape)

        dbn = DBNFeatureExtractor()        
        dbn.train(train_data)
        dbn.save()
    elif sys.argv[1] == "test":
        dbn = DBNFeatureExtractor(load=True)
        test_data = np.array(mp3preprocess("cvrl-subterfuge.mp3"))
        features = dbn.extractFeatures(test_data)
        x,y = zip(*features)
        plt.scatter(y, x, c=range(len(features)))
        plt.show()
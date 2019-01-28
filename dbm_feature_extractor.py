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
    try:
        print(path)
        sound = AudioSegment.from_file(file=path)
        mono = sound.split_to_mono()[0] # TODO maybe concat both sides to have more mono data
        mono = mono.set_frame_rate(SAMPLE_RATE)
        bit_depth = mono.sample_width * 8
        array_type = get_array_type(bit_depth)
        numeric_array = np.array(array.array(array_type, mono._data))
        numeric_array = numeric_array[:-(len(numeric_array)%NSAMPLES)]
        frames = np.array_split(numeric_array, len(numeric_array)/NSAMPLES)
        frames = map(partial(np.fft.fft, norm="ortho"), frames)
        frames = [f[:NSAMPLES//2 +1] for f in frames]
        frames = map(np.absolute, frames)
        frames = [f/NSAMPLES for f in frames]
        return np.array(list(frames))
    except:
        print("Error "+path)
        return None
    


from dbn.tensorflow import UnsupervisedDBN
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt

class DBNFeatureExtractor(object):
    def __init__(self, load=False):
        if load:
            self.dbn = UnsupervisedDBN.load("dbn.pickle")
            self.prepca = pickle.load(open("prepca.pickle", "rb"))
            self.pca = pickle.load(open("pca.pickle", "rb"))
        else:
            self.dbn = UnsupervisedDBN(hidden_layers_structure=[50, 50, 50],
                                       batch_size=1024,
                                       learning_rate_rbm=0.001,
                                       n_epochs_rbm=5,
                                       contrastive_divergence_iter=1,
                                       activation_function='sigmoid')
            self.prepca = PCA(n_components=160)
            self.pca = PCA(n_components=2)
    def save(self):
        self.dbn.save("dbn.pickle")
        pickle.dump(self.prepca, open("prepca.pickle", "wb"))
        pickle.dump(self.pca, open("pca.pickle", "wb"))

    def train(self, frames):
        frames = self.prepca.fit_transform(frames)
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
        frame = self.prepca.transform(frame)
        raw_features = self.dbn.transform(frame)
        return self.pca.transform(raw_features)

if __name__ == "__main__":
    TRAIN_DATA_PATH = "./traindata"
    dbn = None
    if sys.argv[1] == "train":
        paths = []
        for root, dirs, files in os.walk(TRAIN_DATA_PATH):  
            for filename in files[:10]:
                if filename[-4:] == ".mp3":
                    paths.append(TRAIN_DATA_PATH+"/"+filename)
        p = Pool(8)
        train_data = p.map(mp3preprocess, paths)
        train_data = [d for d in train_data if d is not None]
        print("Data preprocessing done")
        train_data = np.concatenate(np.array(train_data))
        print(train_data.shape)

        dbn = DBNFeatureExtractor()        
        dbn.train(train_data)
        dbn.save()
    elif sys.argv[1] == "test":
        dbn = DBNFeatureExtractor(load=True)
        test_data = np.array(mp3preprocess("traindata/01 REC-2018-12-02.mp3"))
        features = dbn.extractFeatures(test_data)
        #features = np.mean(np.split(features[:5000], 500), axis=1)
        #print(features)
        x,y = zip(*features)
        plt.scatter(y, x,c=np.arange(len(x)),  cmap="viridis", marker="x")
        plt.autoscale()
        plt.show()
    elif sys.argv[1] == "fft":
        test_data = np.array(mp3preprocess("cvrl-subterfuge.mp3"))
        fftdata = test_data[200]
        n = len(fftdata)
        k = np.arange(n)
        T = n/SAMPLE_RATE
        frq = k/T
        plt.plot(frq, fftdata,  'r')
        plt.show()
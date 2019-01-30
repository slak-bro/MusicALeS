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
import matplotlib.animation as animation

class DBNFeatureExtractor(object):
    def __init__(self, load=False):
        if load:
            self.bands = pickle.load(open("bands.pickle", "rb"))
            self.dbn = UnsupervisedDBN.load("dbn.pickle")
            self.prepca = pickle.load(open("prepca.pickle", "rb"))
            self.pca = pickle.load(open("pca.pickle", "rb"))
        else:
            self.dbn = UnsupervisedDBN(hidden_layers_structure=[50, 50, 50],
                                       batch_size=4096,
                                       learning_rate_rbm=0.001,
                                       n_epochs_rbm=15,
                                       contrastive_divergence_iter=1,
                                       activation_function='sigmoid')
            self.bands = [
                {"start": 0, "end": 150, "pca_components":30},
                {"start": 120, "end":300, "pca_components":70},
                {"start": 250, "end":513, "pca_components":60}
            ]
            self.prepca = [PCA(n_components=band["pca_components"]) for band in self.bands]
            self.pca = PCA(n_components=16)
    def save(self):
        self.dbn.save("dbn.pickle")
        pickle.dump(self.bands, open("bands.pickle", "wb"))
        pickle.dump(self.prepca, open("prepca.pickle", "wb"))
        pickle.dump(self.pca, open("pca.pickle", "wb"))

    def train(self, frames):
        frames = [self.prepca[bandIndex].fit_transform(frames[:,band["start"]:band["end"]]) 
                             for bandIndex, band  in enumerate(self.bands)]
        frames = np.concatenate(frames, axis=1)
        print(frames.shape)
        self.dbn.fit(frames)
        raw_features = self.dbn.transform(frames)
        self.pca.fit(raw_features)

    def extractFeatures(self, frames):
        frames = [self.prepca[bandIndex].transform(frames[:,band["start"]:band["end"]]) 
                             for bandIndex, band  in enumerate(self.bands)]
        frames = np.concatenate(frames, axis=1)
        raw_features = self.dbn.transform(frames)
        return self.pca.transform(raw_features)

from pydub.playback import play
from multiprocessing import Process
import time
def mp3_real_time_plot(path, featureExtractor):
    frames_data = mp3preprocess(path)
    features_data = featureExtractor.extractFeatures(np.array(frames_data))
    segment = AudioSegment.from_file(file=path)
    segment_duration = len(segment)/1000
    fig = plt.figure()
    dim = 16
    ax = [fig.add_subplot(4, 4, i+1) for i in range(dim)]
    xs = []
    ys = [[] for _ in range(dim)]
    
    start_time = time.time()
    play_process = Process(target=play, args=(segment,))
    play_process.start()
    # This function is called periodically from FuncAnimation
    def animate(i, xs, ys):
        play_time = time.time() - start_time
        frameIndex = int(play_time * SAMPLE_RATE) // NSAMPLES
        if frameIndex >= len(features_data):
            return
        #current_features = features_data[frameIndex]
        ys = np.transpose(features_data[max(0,frameIndex-1000):frameIndex+1])
        xs = range(len(ys[0]))
        #xs = xs[-100:]
        plt.title('PCA over Time')
        #xs.append(play_time)
        for i in range(dim):
            #ys[i].append(current_features[i])
            #ys[i] = ys[i][-100:]
            # Draw x and y lists
            ax[i].clear()
            ax[i].plot(xs, ys[i])
            ax[i].set_title("PCA[{}]".format(i))
            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=500)
    plt.show()



if __name__ == "__main__":
    TRAIN_DATA_PATH = "./traindata"
    dbn = None
    if sys.argv[1] == "train":
        paths = []
        for root, dirs, files in os.walk(TRAIN_DATA_PATH):  
            for filename in files[:5]:
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
        test_data = np.array(mp3preprocess("/home/arthur/Documents/BeatDetectionArduinoEngine/cvrl-subterfuge.mp3"))
        features = dbn.extractFeatures(test_data)
        #features = np.mean(np.split(features[:5000], 500), axis=1)
        #print(features)
        x,y = zip(*features)
        plt.scatter(y, x,c=np.arange(len(x)),  cmap="viridis", marker="x")
        plt.autoscale()
        plt.show()
    elif sys.argv[1] == "rttest":
        dbn = DBNFeatureExtractor(load=True)
        mp3_real_time_plot(sys.argv[2], dbn)
    elif sys.argv[1] == "fft":
        test_data = np.array(mp3preprocess("cvrl-subterfuge.mp3"))
        fftdata = test_data[200]
        n = len(fftdata)
        k = np.arange(n)
        T = n/SAMPLE_RATE
        frq = k/T
        plt.plot(frq, fftdata,  'r')
        plt.show()
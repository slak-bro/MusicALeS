from yaafelib import *

fp = FeaturePlan(sample_rate=44100)
fp.addFeature('bpm: AutoCorrelationPeaksIntegrator ACPInterPeakMinDist=5  ACPNbPeaks=50  ACPNorm=BPM  NbFrames=800  StepNbFrames=30')
df = fp.getDataFlow()

engine = Engine()
engine.load(df)

afp = AudioFileProcessor()
afp.processFile(engine, "test.wav")

feats = engine.readAllOutputs()
import ipdb; ipdb.set_trace()

afp.setOutputFormat('txt', 'output', {"Precision":'8'})
afp.processFile(engine, "test.wav")
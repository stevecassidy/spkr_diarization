# Script to interpret diarization results on a audio file. 
import numpy as np
from scipy.io import wavfile
import pylab


def add_wgn(s,var=1e-4):
    """ Add white Gaussian noise to signal
        If no variance is given, simply add jitter. 
        This is for numerical stability purposes. """
    noise = np.random.normal(0,var,len(s))
    np.random.seed(0)
    return s + noise

def read_wav(filename):
    """
        read wav file. 
        Normalizes signal to values between -1 and 1. 
        Also add some jitter to remove all-zero segments."""
    fs, s = wavfile.read(filename) # scipy reads int
    s = np.array(s)/float(max(abs(s)))
    s = add_wgn(s) # Add jitter for numerical stability
    return fs,s

def time_to_sample(time_stamp,fs):
    """
       Convert time value in seconds to sample. """
    return 1 + int(time_stamp/float(fs))

def list_to_array(in_list):
    """
       Convert 1D list of numeric values to np array. 
       Added this because I had to use it several times. """
    out_array = np.array(in_list)
    return out_array[:]

def segs_to_stream(labels,segment_starts,segment_ends):
    """
       Compress labels, their start times, and their end times 
       into a single numpy array. This is for plotting purposes.
        """
    N = segment_ends[-1]
    stream = np.zeros((1,N))
    for i in range(len(labels)):
        stream[segment_starts[i]:segment_ends[i]] = labels[i]
    return stream

def read_segs(filename, fs=16000.0):
    """
        read segment file.
        Uses the segment file format defined by AudioSeg. 
        lines contain three fields:
        label start_time end_time
    """
    # For SAD segments, labels are limited ot sil and speech.
    # Other segments, use different label values. 
    # NOTE: will have to add conditions for cluster and bic segments. 
    fin = open(filename)
    labels = []
    segment_starts = []
    segment_ends = []
    for i in fin:
        line = i.strip()
        line_list = line.split(' ')
        if line_list[0]=='sil':
            labels.append(0)
        elif line_list[0]=='speech':
            labels.append(1)
        segment_starts.append(time_to_sample(str(line_list[1].strip()),fs))
        segment_ends.append(time_to_sample(str(line_list[2].strip()),fs))
    fin.close()
    labels = list_to_array(in_list)
    segment_starts = list_to_array(segment_starts)
    segment_ends = list_to_array(segment_ends)
    label_stream = segs_to_stream()
    return label_stream
if __name__=='__main__':
    fname='/home/navid/data/ami_sample/amicorpus/ES2002a/audio/ES2002a.Mix-Headset.wav'
    fs,s = read_wav(fname)
    segname='/home/navid/spkr_diarization/test_audioseg/out_dir/ES2002a.sad'
    labels = read_segs(segname,fs)
    pylab.plot(s)
    pylab.plot(labels)
    pylab.show()





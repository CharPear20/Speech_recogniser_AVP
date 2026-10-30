# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 14:40:57 2026

@author: Pears
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import soundfile as sf
import sounddevice as sd
import plotly.io as pio
import plotly.express as px
import scipy as spy
# this is the beginning of the coursework this is where the 
# wav files go through the process of being turned into feature vectors





def magPhase(speechFrame, hamming):
    # we take the speechframe
    # step 1: hamming window the speech frame
    # speechFrame is a numPy array of our audio signal
    
    
    # 320 samples in one 20ms window
    window = np.hamming(hamming)
    
    windowed_frame = window * speechFrame
    #plt.plot(windowed_frame)
    
    # now that we have hammed the frame 
    # we can now use DFT
    # or FFT in this case
    
    wFrame_FFT = np.fft.fft(windowed_frame)
    
    # FFT does produce complex numbers
    #print(wFrame_FFT[1])
    #print(np.imag(wFrame_FFT))
    #print(np.real(wFrame_FFT))
    #plt.plot(wFrame_FFT)
    #plt.show()
    
    
    # then get the mag spec
    
    shortTimeMag = np.abs(wFrame_FFT)
    shortTimePhase = np.angle(wFrame_FFT)
    
    #plt.plot(magSpec)
    #plt.plot(phaseSpec)
    
    #figures, axes = plt.subplots(2,1)
    #axes[0].plot(shortTimeMag)
    #axes[1].plot(shortTimePhase)
    #plt.show()
    
    
    return shortTimeMag, shortTimePhase


    
def linear_filterbank(magSpec):
    print("Beginning linear filterbank")
    #Hyper parameter for this function
    filterbank_channels = 5
    # ----------------------------------------------------
    # I initially want to implement the simplest version
    # of the filterbank so that i can gradually step up to 
    # the mel spec frequency cepstral coefficient filterbank
    # ----------------------------------------------------
    # only need the first half samples so can drop the 
    # second half
    # ----------------------------------------------------
    # due to nyquist theorem i can only use half of the 
    # total plotted points
    # plotting the magspec
    half_magspec = int(magSpec.size/2)
    useful_magspec = magSpec[:half_magspec]
    #print(useful_magspec.size)
    #plt.plot(useful_magspec)
    #plt.show()
    # ----------------------------------------------------
    #fbank = np.zeros(filterbank_channels)
    
    
    # ----------------------------------------------------
    # this needs to be fixed but for now it works on this 
    fbank = np.zeros(filterbank_channels)
    for i in range(filterbank_channels):
        #fbank[i] = sum(useful_magspec[32*(i-1):32*i])
        fbank[i] = sum(useful_magspec[32*(i):32*(i+1)])
    # ----------------------------------------------------
        
        
    return fbank

def linear_filterbank_matrix(magSpec):
    print("Beginning linear filterbank with Matrix multiplication")
    
    half_magspec = int(magSpec.size/2)
    useful_magspec = magSpec[:half_magspec]
    
    
    # the way i am doing this is redundant 
    # could be a matrix of 160 columns and 
    # the same amount of rows that you would 
    # have for the filterbank channels
    
    # i also need to add more filter channels
    one = np.zeros(160)
    one[0:32] = 1
    
    two = np.zeros(160)
    two[32:64] = 1
    
    three = np.zeros(160)
    three[64:96] = 1
    
    four = np.zeros(160)
    four[96:128] = 1
    
    five = np.zeros(160)
    five[128:160] = 1


    f_bank = np.zeros(5)

    f_bank[0] = np.matmul(one, useful_magspec)
    f_bank[1] = np.matmul(two,useful_magspec)
    f_bank[2] = np.matmul(three, useful_magspec)
    f_bank[3] = np.matmul(four,useful_magspec)
    f_bank[4] = np.matmul(five, useful_magspec)
    
    
    
    
    return f_bank
    
    
    
    

def mel_scaled_filterbank(magSpec):
    #print("Beginnning mel scaled filterbank")
    
    # dont forget to half the magSPEC!!!!!!!!!!!!!!!!!!!!!!!!!!!
    half_magspec = int(magSpec.size/2)
    useful_magspec = magSpec[:half_magspec]
    
    #step 1) determine the minimum and maximum frequencies 
    #the magspec displays
    filter_channels = 22 # this is +2 than what i actually have
    minimum_frequency = 0
    maximum_frequency = 16000/2
    # ----------------------------------------------------
    # step 2) convert these values onto the melscale
    mel_minimum = 1125 * np.log(1+minimum_frequency/700)
    mel_maximum = 1125 * np.log(1+maximum_frequency/700)
    # ----------------------------------------------------
    # step three is determining how many filters you want
    # and then add 2 more filters to it
    #mel_scale_filterbank_channels = 7
    #print(mel_maximum)
    # now calculate equal parts from each of these frequencies
    # say i want 7 filters
    
    # calculating the step between each filters
    step_size = (mel_maximum - mel_minimum) / (filter_channels - 1)
    
    melFrequencies = np.zeros(filter_channels)
    for n in range(filter_channels):
        melFrequencies[n] = n * step_size
        
        
        
        
    # now that we have the mel frequencies we need to now turn them
    # back into normal frequencies which can be done using a special 
    # equation
    
    
    mel_to_freq = np.zeros(filter_channels)
    for n in range(filter_channels):
        mel_to_freq[n] = 700 * (np.exp(melFrequencies[n] / 1125) - 1)
        
    
    #print(mel_to_freq)
    # now we need to calculate the bins that the frequencies relate to
    freq_to_bins = np.zeros(filter_channels)
    for n in range(filter_channels):
        bin_number = (160/8000) * mel_to_freq[n]
        freq_to_bins[n] = int(round(bin_number))
       
        
    xpoints = mel_to_freq
    ypoints = melFrequencies
    #plt.plot(xpoints, ypoints)
    #plt.title("Melfrequency to frequency bins")
    #plt.ylabel("Mel Frequencies")
    #plt.xlabel("Frequency")
    #plt.show()
    #print(freq_to_bins)
    # now that we have the corresponding frequency bins we can do 
    # some magic with the basis vectors
    
    
    # ----------------------------------------------------
    # now is the time for calculating the monstrosities that are the 
    # basis vector equations that are needed to finish implementing this
    # type of filterbank
    mfcc_matrix = np.zeros((filter_channels - 2, useful_magspec.size))
    for m in range(1, filter_channels - 1):
        for k in range(useful_magspec.size):
            if k < freq_to_bins[m-1]:
                mfcc_matrix[m-1, k] = 0
            elif freq_to_bins[m - 1] <= k <= freq_to_bins[m]:
                # the part of the triangle before the peak
                mfcc_matrix[m-1, k] = (k - freq_to_bins[m - 1])/(freq_to_bins[m] - freq_to_bins[m-1])
            elif  freq_to_bins[m] <= k <= freq_to_bins[m+1]:
                # the part of the triangle after the peak
                mfcc_matrix[m-1, k] = (freq_to_bins[m+1] - k)/(freq_to_bins[m+1] - freq_to_bins[m])
            elif k > freq_to_bins[m+1]:
                mfcc_matrix[m-1, k] = 0
            
    
    
    
    # ----------------------------------------------------
    # need to transpose the values for the matrix
    transposed_mfcc_matrix = mfcc_matrix.transpose()
    
    #plt.plot(transposed_mfcc_matrix)
    #plt.show()
    #print(mfcc_matrix.shape)
    #print(mfcc_matrix)
    
    
    
    
    feature_vector = np.matmul(transposed_mfcc_matrix.T, useful_magspec)
    
    #plt.plot(feature_vector)
    #plt.show()
    
    # ----------------------------------------------------
    # now it is time to log the values of the feature vector
    epsilon = 1e-10
    logged_feature_vector = np.log(feature_vector + epsilon)
    
    # ----------------------------------------------------
    # now we have to apply the dct function to the 
    # logged feature vectors
    #return  spy.fft.dct(logged_feature_vector)
    return  spy.fft.dct(logged_feature_vector)
    # ----------------------------------------------------
    
    
        

    
    
    
    



def getting_wav_files():
    print("Getting wavfiles")
    # ----------------------------------------------------
    # these are variables that are necessary to get the wav files from each
    sample_rate = 16000
    # gets the full audio file
    recorded_data_directory = Path.cwd().absolute()
    wav_files = recorded_data_directory / "recorded_wav_files"
    mono_files = wav_files / "mono_files"
    # ----------------------------------------------------
    # every file needs to be the same length so that they can 
    # go into the neural network without any issue 
    # the longest duration is below, which means the maximum
    # total of samples in any file is 3.3*16000 so numpy array 
    # extracted from each file needs to be made to be the same 
    # length
    # longest_duration for a file was 3.3 seconds
    maximum_total_samples = int(3.3*16000)
    # should equal 52800 which is a yikes but luckily all of it 
    # gets halved
    # ----------------------------------------------------
    # now we iterate through every file in the mono directory and 
    # apply the feature extraction on every frame in the file
    # and then store the feature vectors in labelled matrixes 
    # ready to be fed into the Deep neural network
    # ----------------------------------------------------
    # for every file in the mono folder get it
    
    #for wav_path in sorted(mono_files.glob("*.wav")):
    #    # read the current file
    #    wav_file, sample_rate = sf.read(wav_path,dtype='float32')
    #    
        # need to pad each mono file to the same length
        # as they are all arrays you can treat them like arrays of numbers
    #    if len(wav_file) < maximum_total_samples:
    #        wav_file = np.pad(wav_file, (0, maximum_total_samples - len(wav_file)))
    #    else:
    #        wav_file = wav_file[:maximum_total_samples]
        # ----------------------------------------------------
        # starting the feature extraction, 
        # this should return 
        #feature_extraction(wav_file,duration,sample_rate)
        
            
            #features_list.append(features)
            #file_names.append(wav_path.name)
            #labels.append(wav_path.stem.split("_")[0])  # e.g. "Aaron_R1" -> "Aaron"
        
            #X = np.array(features_list)
            #y = np.array(labels)
        # ----------------------------------------------------
        
    Aaron_recorded = mono_files / "Aaron_R1.wav"
    wav_file, sample_rate = sf.read(Aaron_recorded,dtype='float32')
    duration = len(wav_file) / sample_rate
    frame_length = 320
    hop_length = frame_length // 2
        
    # frame vectors will store 329 lots of 20 feature vectors
        
    frame_vectors=[]
    if len(wav_file) < maximum_total_samples:
            wav_file = np.pad(wav_file, (0, maximum_total_samples - len(wav_file)))
    else:
            wav_file = wav_file[:maximum_total_samples]
        
    for start in range(0, len(wav_file) - frame_length + 1, hop_length):
        frame = wav_file[start: start + frame_length]
        
            
            
        feature_vector = feature_extraction(frame,duration,sample_rate)
        frame_vectors.append(feature_vector)
        
    mfcc_for_aaron = np.array(frame_vectors)
    plt.imshow(mfcc_for_aaron)
    for n in mfcc_for_aaron:
        print(n)
    
    
    features_path = recorded_data_directory / "features"
    
    
    
    print(mfcc_for_aaron.shape)
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    



def feature_extraction(frame,duration, sample_rate):
    #print("Beginning feature extraction")
    
    # ----------------------------------------------------
    # a single frame is being sent to this file
    # ----------------------------------------------------
    # calculating total samples in the file
    #total_samples = int(sample_rate * duration)
    #print(f"Total number of samples in the wav file: {total_samples}")
    # ----------------------------------------------------
    #calculating samples per window
    samples_per_window = int(0.02*sample_rate)
    #print(f"Total number of samples per window: {samples_per_window}")
    # ----------------------------------------------------
    #calculating total number of windows
    #total_windows = int(total_samples/samples_per_window)
    #print(f"Total number of windows: {total_windows}")
    # ----------------------------------------------------
      
    #pio.renderers.default='browser'
    
    #fig = px.line(wav_file)
    #fig = px.line(wav_file[numbers_to_slice[0]:numbers_to_slice[1]])
    #fig.show()
    
    #plt.plot(wav_file[numbers_to_slice[0]:numbers_to_slice[1]])
    #plt.plot(wav_file[numbers_to_slice[5]:numbers_to_slice[6]])
    # ----------------------------------------------------
    # now need to go through each frame of the file and 
    
    
    magSpec, phaseSpec= magPhase(frame, samples_per_window)
    
    
    
    
    
    
    
    
    
    # ----------------------------------------------------
    # now time for the filterbank section of feature extraction
    # take the magspec and apply the filterbank to generate 
    # feature vectors
    # ----------------------------------------------------
    
    #plt.plot(magSpec)
    #plt.show()
    #f_bank = np.array(linear_filterbank(magSpec))
    
    #print(f"fbank shape: {f_bank.shape}")
    
    
    # 8 is also the amount of filterbank channels
    #feature_vector = np.zeros((total_windows,8))
    
    #feature_vector[0] = f_bank
    #print(feature_vector)
    # ----------------------------------------------------
    # trying to implement the linear filterbank with matrix
    # multiplication
    #plt.plot(linear_filterbank_matrix(magSpec))
    #print(linear_filterbank_matrix(magSpec))
    #plt.plot(linear_filterbank(magSpec))
    #print(linear_filterbank(magSpec))
    #plt.show()
    
    # ----------------------------------------------------
    # we now have a feature vector for a single frame
    # this is really where we need to generate all of them for a file
    # i need all of these for a given file
    feature_vector = mel_scaled_filterbank(magSpec)
    #print(feature_vector)
    return feature_vector















getting_wav_files()



















# vowel has a fs of 16000 for 5 seconds so it has 
# 80000 total points in the array
#speechFrame = sf.read('Vowel.wav',dtype='float32')


#audio_signal = speechFrame[0]
#should normalise audio before framing it
#speechFrame = audio_signal[1000:1320]
#plt.plot(speechFrame)
#magAndPhase(speechFrame)
#sd.play(wav_file, 16000)

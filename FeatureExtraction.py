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
    
    
    
    

def mel_scaled_filterbank(magSpce):
    print("Beginnning mel scaled filterbank")
    
    #step 1) determine the minimum and maximum frequencies 
    #the magspec displays
    minimum_frequency = 0
    maximum_frequency = 16000/2
    # ----------------------------------------------------
    # step 2) convert these values onto the melscale
    mel_minimum = 1125 * np.log(1+minimum_frequency/700)
    mel_maximum = 1125 * np.log(1+maximum_frequency/700)
    # ----------------------------------------------------
    # step three is determining how many filters you want
    # and then add 2 more filters to it
    mel_scale_filterbank_channels = 7
    # now calculate 
    
    
    
def log_dct(fbank):
    print("Completing the log and dct after the filterbank")


def getting_wav_files():
    print("Getting wavfiles")
    sample_rate = 16000
    # gets the full audio file
    recorded_data_directory = Path.cwd().absolute()
    wav_files = recorded_data_directory / "recorded_wav_files"
    mono_files = wav_files / "mono_files"
    Aaron_recorded = mono_files / "Aaron_R1.wav"
    
    
    
    wav_file, sample_rate = sf.read(Aaron_recorded,dtype='float32')
    
    duration = len(wav_file) / sample_rate
    
    
    
    # then need to start feature extraction
    
    feature_extraction(wav_file,duration,sample_rate)
    
    
    



def feature_extraction(wav_file,duration, sample_rate):
    print("Beginning feature extraction")
    
    # ----------------------------------------------------
    #to do list
    # - add 50% overlap on frames before hamming the window
    #
    # ----------------------------------------------------
    # calculating total samples in the file
    total_samples = int(sample_rate * duration)
    print(f"Total number of samples in the wav file: {total_samples}")
    # ----------------------------------------------------
    #calculating samples per window
    samples_per_window = int(0.02*sample_rate)
    print(f"Total number of samples per window: {samples_per_window}")
    # ----------------------------------------------------
    #calculating total number of windows
    total_windows = int(total_samples/samples_per_window)
    print(f"Total number of windows: {total_windows}")
    # ----------------------------------------------------
    # now we need to split this wav file into frames
    numbers_to_slice = []
    for i in range(total_windows):
        numbers_to_slice.append(samples_per_window*(i+1))
    # ----------------------------------------------------
    # this isnt doing too much it is literally just spewing 
    # out the contents of the array, so that i can see them
    #for n in numbers_to_slice:
    #    print(n)
    # ----------------------------------------------------
    #testing the slicing stuff on one frame
    #with no 50% overlap yet
    
    #pio.renderers.default='browser'
    
    #fig = px.line(wav_file)
    #fig = px.line(wav_file[numbers_to_slice[0]:numbers_to_slice[1]])
    #fig.show()
    
    #plt.plot(wav_file[numbers_to_slice[0]:numbers_to_slice[1]])
    #plt.plot(wav_file[numbers_to_slice[5]:numbers_to_slice[6]])
    # ----------------------------------------------------
    # now slice the audio file according to the values in the array
    #for i in range(total_windows):
        # get the window and then apply the feature extraction
    
    magSpec, phaseSpec= magPhase(wav_file[numbers_to_slice[0]:numbers_to_slice[1]], samples_per_window)
    
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
    mel_scaled_filterbank(magSpec)
    















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

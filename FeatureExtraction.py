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
# this is the beginning of the coursework this is where the 
# wav files go through the process of being turned into feature vectors


def getting_wav_files(sample_rate):
    print("Getting wavfiles")
    
    # gets the full audio file
    recorded_data_directory = Path.cwd().absolute()
    wav_files = recorded_data_directory / "recorded_wav_files"
    Aaron_recorded = wav_files / "Aaron_R1.wav"
    
    
    
    wav_file, sample_rate = sf.read(Aaron_recorded,dtype='float32')
    
    duration = len(wav_file) / sample_rate
    
    
    
    # then need to start feature extraction
    
    feature_extraction(wav_file,duration,sample_rate)
    
    
    



def feature_extraction(wav_file,duration, sample_rate):
    print("Beginning feature extraction")
    
    total_samples = int(sample_rate * duration)
    print(total_samples)
    
    # ----------------------------------------------------
    #calculating samples per window
    samples_per_window = int(0.02*sample_rate)
    print(samples_per_window)
    # ----------------------------------------------------
    #calculating total number of windows
    total_windows = int(total_samples/samples_per_window)
    print(total_windows)
    
    # ----------------------------------------------------
    # now we need to split this wav file into frames
    numbers_to_slice = []
    for i in range(total_windows):
        numbers_to_slice.append(samples_per_window*(i+1))
    # ----------------------------------------------------
    for n in numbers_to_slice:
        print(n)
    # ----------------------------------------------------
    # now slice the audio file according to the values in the array
    
    
    
def linear_filterbank(magspec, filterbank_channels):
    print("Beginning linear filterbank")
    
    















def magPhase(speechFrame, hamming):
    # we take the speechframe
    # step 1: hamming window the speech frame
    # speechFrame is a numPy array of our audio signal
    
    
    # 320 samples in one 20ms window
    window = np.hamming(hamming)
    
    windowed_frame = window * speechFrame
    plt.plot(windowed_frame)
    
    # now that we have hammed the frame 
    # we can now use DFT
    # or FFT in this case
    
    wFrame_FFT = np.fft.fft(windowed_frame)
    
    # FFT does produce complex numbers
    #print(wFrame_FFT[1])
    #print(np.imag(wFrame_FFT))
    #print(np.real(wFrame_FFT))
    
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


getting_wav_files(16000)



# vowel has a fs of 16000 for 5 seconds so it has 
# 80000 total points in the array
#speechFrame = sf.read('Vowel.wav',dtype='float32')


#audio_signal = speechFrame[0]
#should normalise audio before framing it
#speechFrame = audio_signal[1000:1320]
#plt.plot(speechFrame)
#magAndPhase(speechFrame)
#sd.play(wav_file, 16000)

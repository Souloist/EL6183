# DSP LAB FALL 2015
# Richard Shen
# Assignment 3

import wave
import sys

folderpath = sys.path[0]
filename_full = folderpath + "/" + "16bit.wav"
wf = wave.open(filename_full)

print 'The following parameters for 16bits:\n'
print 'Number of channels: ', wf.getnchannels() 
print 'Framerate: ', wf.getframerate() 
print 'Width of 16bit :', wf.getsampwidth() 
print ''

filename_full = folderpath + "/" + "8bit.wav"
wf = wave.open(filename_full)
print 'The following parameters for 8bits:\n'
print 'Width of 8bit :', wf.getsampwidth() 
print ''

filename_full = folderpath + "/" + "32bit.wav"
wf = wave.open(filename_full)
print 'The following parameters for 32bits:\n'
print 'Width of 32bit :', wf.getsampwidth() 
print ''
wf.close()

# DSP LAB FALL 2015
# Richard Shen
# Section 2 Exercise 3

import pyaudio
import math
import struct
import numpy as np
from scipy import signal
from numpy import transpose
import cmath
from matplotlib import pyplot as plt

def clip16( x ):    
    # Clipping for 16 bits
    if x.all() > 32767:
        x = 32767
    elif x.all() < -32768:
        x = -32768
    else:
        x = x      
    return int(x)

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000        # Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 10  		# Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(-10000, 10000)        # set y-axis limits

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Time (n)')
t = range(0, BLOCKSIZE)

# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)

i = cmath.sqrt(-1)

# Copied complex coefficients from MATLAB demo05.m file

a = [1.0 + 0.0j, -0.0 - 1.2762j, -2.6471 + 0.0j, 0.0 + 2.2785j, 2.1026 - 0.0j, \
	-0.0 - 1.1252j, -0.4876 + 0.0j, 0.0 + 0.1136j]
b = [0.0423 + 0.0j, 0.0 + 0.1193j, -0.2395 + 0.0j, -0.0 - 0.3208j, .3208 - 0.0j,  \
	0.0 + 0.2395j, -0.1193 + 0.0j, -0.0 - 0.0423j]

fs = RATE                   # Sampling frequency
f1 = 400;
output_filt = [0 for i in range(BLOCKSIZE)]
complexAM = [0 for i in range(BLOCKSIZE)]
output_tuple = [0 for i in range(BLOCKSIZE)]


# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * np.pi

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

for j in range(0, NumBlocks):

    input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert

    # Calculating the different equation using the filter function from scipy
    output_filt = signal.lfilter(b,a, input_tuple)

    # Calculating the complex AM
    complexAM = [ np.exp( 2j * np.pi * f1 * t/fs) for t in range(BLOCKSIZE) ]

    # Applying the complex AM to the filter
    output_tuple = output_filt * complexAM

    # Keeping the real parts of the complex AM
    output_tuple = output_tuple.real

    # Set angle for next block
    theta = theta + theta_del

    # Clip and convert output value to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_tuple)

    # Write output to audio stream
    stream.write(output_string)
# plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'

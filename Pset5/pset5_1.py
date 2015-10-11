# DSP LAB FALL 2015
# Richard Shen
# Section 1 Exercise 3

import pyaudio
import struct
import math

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio

BLOCKSIZE = 64  # Number of frames per block

WIDTH = 2       # Number of bytes per sample
CHANNELS = 2    # stereo
RATE = 32000    # Sampling rate (samples/second)
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

number_of_devices = p.get_device_count()
print('There are {0:d} devices'.format(number_of_devices))

property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
for i in range(0, number_of_devices):
    print('Device {0:d} has:'.format(i))
    for s in property_list:
        print ' ', s, '=', p.get_device_info_by_index(i)[s]

stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

output_block = [0 for i in range(0, 2*BLOCKSIZE)] # output block is twice as large because there are two channels

# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi

# Number of blocks to run for
num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

print('* Recording for {0:.3f} seconds'.format(RECORD_SECONDS))

# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    input_string = stream.read(BLOCKSIZE)       # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)
   
    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation:
        output_block[2*n] = clip16(input_tuple[2*n] * 2*math.cos(2*math.pi*n*f0/RATE + theta)) # Right earphone processing
        output_block[2*n+1] = clip16(input_tuple[2*n+1] * math.cos(2*math.pi*n*f0/RATE + theta)) # Left earphone processing


    # Set angle for next block
    theta = theta + theta_del

    # Convert values to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

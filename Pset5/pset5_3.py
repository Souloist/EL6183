# DSP LAB FALL 2015
# Richard Shen
# Section 2 Exercise 4

import pyaudio
import wave
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

wavfile = 'author.wav'
# wavfile = 'decay_cosine_mono.wav'
print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato and flanger parameters
f0 = 2
W = 0.2         # W = 0  for no vibrato effct
Gdp = 0.8        # Gdp = 0 for no flanger effect 

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw = buffer_MAX/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

output_all = ''            # output signal in all (string)

print ('* Playing...')

# Loop through wave file 
for n in range(0, LEN):

    # Get sample from wave file
    input_string = wf.readframes(1)

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]
    print input_value
    # Get previous and next buffer values (since kr is fractional)
    kr_prev = int(math.floor(kr))               
    kr_next = kr_prev + 1
    frac = kr - kr_prev    # 0 <= frac < 1
    if kr_next >= buffer_MAX:
        kr_next = kr_next - buffer_MAX

    # Compute output value using interpolation
    output_value = Gdp * input_value + (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]  # In the flanger effect, there is a direct path 

    # Update buffer (pure delay)
    buffer[kw] = input_value

    # Increment read index
    kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        # Note: kr is fractional (not integer!)

    # Ensure that 0 <= kr < buffer_MAX
    if kr >= buffer_MAX:
        # End of buffer. Circle back to front.
        kr = 0

    # Increment write index    
    kw = kw + 1
    if kw == buffer_MAX:
        # End of buffer. Circle back to front.
        kw = 0
    #print output_value
    # Clip and convert output value to binary string
    output_string = struct.pack('h', clip16(output_value))

    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
# DSP LAB FALL 2015
# Richard Shen
# Section 2 Exercise 3

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

# Vibrato parameters
f_left = 2              # Frequency of left ear
f_right = 3             # Frequency of right ear
W_right = 0.2           # Amplitude of right
W_left = 0.2            # Amplitude of left

BLOCKSIZE = 64          # Number of frames per block
CHANNELS = 2            # stereo
RATE = 32000            # Sampling rate (samples/second)
RECORD_SECONDS = 5      # Recording time 

# Create a buffer (delay line) for past values
buffer_MAX =  1024                                  # Buffer length
buffer_left = [0.0 for i in range(buffer_MAX)]      # Buffer to store left values
buffer_right = [0.0 for i in range(buffer_MAX)]     # Buffer to store right values

# Buffer (delay line) indices
kr_left = 0
kr_right = 0                      # read index
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True )


output_block = [0 for i in range(0, 2*BLOCKSIZE)]

# Initialize angle
theta_left = 0.0
theta_right = 0.0

# Block-to-block angle increment
theta_del_left = (float(BLOCKSIZE*f_left)/RATE - math.floor(BLOCKSIZE*f_left/RATE)) * 2.0 * math.pi
theta_del_right = (float(BLOCKSIZE*f_right)/RATE - math.floor(BLOCKSIZE*f_right/RATE)) * 2.0 * math.pi

# Number of blocks to run for
num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

print('* Recording for {0:.3f} seconds'.format(RECORD_SECONDS))
new_n = 0 # This value keeps track of n so it is constantly incrementing similiar to theta

# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    input_string = stream.read(BLOCKSIZE)       # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)

    # Go through block
    for n in range(0, BLOCKSIZE):
        # Get previous and next buffer values (since kr is fractional)
        # For the left side
        kr_prev_left = int(math.floor(kr_left))               
        kr_next_left = kr_prev_left + 1
        frac_left = kr_left - kr_prev_left    # 0 <= frac < 1
        if kr_next_left >= buffer_MAX:
            kr_next_left = kr_next_left - buffer_MAX

        # For the right side
        kr_prev_right = int(math.floor(kr_right))               
        kr_next_right = kr_prev_right + 1
        frac_right = kr_right - kr_prev_right    # 0 <= frac < 1
        if kr_next_right >= buffer_MAX:
            kr_next_right = kr_next_right - buffer_MAX

        # Compute output value using interpolation
        output_block[2*n] = clip16((1-frac_right) * buffer_right[kr_prev_right] + frac_right * buffer_right[kr_next_right]) # Right earphone processing
        output_block[2*n+1] = clip16((1-frac_left) * buffer_left[kr_prev_left] + frac_left * buffer_left[kr_next_left]) # Left earphone processing

        # Update buffer (pure delay)
        buffer_right[kw] = input_tuple[2*n]
        buffer_left[kw] = input_tuple[2*n+ 1]

        # Increment read index
        kr_left = kr_left + 1 + W_left * math.sin( 2 * math.pi * f_left * n / RATE +theta_left) # Increments index for left
        kr_right = kr_right + 1 + W_right * math.sin( 2 * math.pi * f_right * n / RATE +theta_right) # Increments index for right 

        # Ensure that 0 <= kr < buffer_MAX
        # For left side
        if kr_left >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr_left = 0

        # For right side
        if kr_right >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr_right = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0
        new_n+=1

    # Set angle for next block
    theta_left = theta_left + theta_del_left
    theta_right = theta_right + theta_del_right
    # Convert values to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
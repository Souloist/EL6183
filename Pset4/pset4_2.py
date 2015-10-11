# DSP LAB FALL 2015
# Richard Shen
# Assignment 2

import pyaudio
import wave
import struct
import math

def clip16( x ):    
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

wavfile = "stereo.wav"

print("Play the wave file %s." % wavfile)

wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

# Set parameters of delay system
Gfb = 0.9        # feed-back gain
Gdp = 0.8        # direct-path gain
Gff = 0.3        # feed-forward gain
# Gff = 0.0      # feed-forward gain

# Create 2 delays
delay_sec_1 = 0.05  # 50 miliseconds
delay_sec_2 = 0.05
delay_samples_1 = int(math.floor(Fs * delay_sec_1))
delay_samples_2 = int(math.floor(Fs * delay_sec_2))

p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )

input_string = wf.readframes(1)          # Get first frame

# Creating two buffers of zeros and setting j and k to 0

buffer_length_1 = delay_samples_1
buffer_1 = [ 0 for i in range(buffer_length_1)]
buffer_length_2 = delay_samples_2
buffer_2 = [ 0 for i in range(buffer_length_2)]
j = 0
k = 0

print("**** Playing ****")
output_value_1 = 0
output_value_2 = 0
while input_string != '':

    # Convert string to number
    input_tuple = struct.unpack('hh', input_string)
    output_value_1 = clip16( Gdp * (input_tuple[0] + output_value_2) + Gff * buffer_1[j]) # The output of the first value is a function of the input and the output of the other channel 
    output_value_2 = clip16( Gdp * (input_tuple[1] + output_value_1) + Gff * buffer_2[k]) # Same thing with other output

    # Update buffers
    buffer_1[j] = input_tuple[0] + Gfb * buffer_1[j]
    j = j + 1
    if j == buffer_length_1:
        j = 0

    buffer_2[k] = input_tuple[1] + Gfb * buffer_2[k]
    k = k + 1
    if k == buffer_length_2:
        k = 0    

    # Convert output value to binary string
    output_string_1 = struct.pack('hh', output_value_1, output_value_2)

    # Write output value to audio stream
    stream.write(output_string_1)    
    # Get next frame
    input_string = wf.readframes(1)  

i = 0 # Playing other frames 
while i < len(buffer_1):

    output_value_1 = clip16(Gff* buffer_1[i])
    output_value_2 = clip16(Gff* buffer_2[i])

    output_string = struct . pack ('hh', output_value_1, output_value_2 )

    # Write output value to audio stream
    stream . write ( output_string )
    i+=1

                                          
print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
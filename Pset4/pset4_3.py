# DSP LAB FALL 2015
# Richard Shen
# Assignment 2

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

wavfile = "cool.wav"

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
gain = 1
gain_delay = 0.8
delay_sec = 0.2 # 50 milliseconds
delay_samples = int(math.floor(Fs * delay_sec))
print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
# Create a buffer to store past values . Initialize to zero .
buffer = [ 0 for i in xrange(delay_samples)]

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )

# Get first frame (sample)
input_string = wf.readframes(1)

k = 0 		# buffer index (circular index)

print (" **** Playing **** ")
count = 0
frames = 0
while frames < signal_length:
	frames +=1
	# Convert string to number
	input_value = struct.unpack ('h', input_string ) [0]

	# Compute output value
	output_value = gain * input_value + gain_delay * buffer [k] 
	output_value = clip16 ( output_value )

	# Update buffer
	buffer [k] = input_value
	k = k + 1
 	if k >= delay_samples:
 		k = 0
 		count+=1
 	# Convert output value to binary string
 	output_string = struct . pack ('h', output_value )

 	# Write output value to audio stream
 	stream . write ( output_string )

 	# Get next frame ( sample )
 	input_string = wf.readframes(1)

leftover = signal_length - count*delay_samples 	
print "This iterates %d times through the buffer" %count
print "There are %d frames leftover" %leftover

i = 0
while i < len(buffer):

	output_value = gain_delay* buffer[i]
	output_value = clip16(output_value)

 	output_string = struct . pack ('h', output_value )

 	# Write output value to audio stream
 	stream . write ( output_string )
 	i+=1

print "Done playing %d leftover frames" %leftover
print (" **** Done **** ")
stream.stop_stream()
stream.close()
p.terminate()
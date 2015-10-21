# DSP LAB FALL 2015
# Richard Shen
# Section 1 Exercise 3

import pyaudio
import struct
from matplotlib import pyplot as plt
import wave

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 48000        # Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 0.5 		# Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )


print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(-10000, 10000)        # set y-axis limits

# Time axis in units of milliseconds:
plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
plt.xlabel('Time (msec)')
t = [n*1000/float(RATE) for n in xrange(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)

# Setting up the output file
output_wavefile = 'Room_response.wav'
output_wf = wave.open(output_wavefile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
				channels = CHANNELS,
				rate = RATE,
				input = True,
				output = False)
print "Listening"
array = []
test = True
while test == True:
	input_string = stream.read(BLOCKSIZE)                    # Read audio input stream
	input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)
	# print max(input_tuple) 
	if max(input_tuple) > 18000:
		for i in xrange(0, NumBlocks):
			input_string = stream.read(BLOCKSIZE)                    # Read audio input stream
			input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
			array+=list(input_tuple)
			line.set_ydata(input_tuple)                               # Update y-data of plot
			plt.draw()
			output_wf.writeframes(input_string)
		test = False
		# plt.close()

# print(array)
stream.stop_stream()
stream.close()
p.terminate()

fig = plt.figure(1)
t = xrange(0, NumBlocks*BLOCKSIZE)
plt.plot(t, array)
plt.axis((0, len(array), min(array), max(array)))
plt.xlabel("Number of samples")
plt.ylabel("Magnitude of Frequency Response")
print '* Done'
output_wf.close()

fig.savefig("Room_response.pdf")

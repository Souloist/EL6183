from math import cos, pi 
import pyaudio
import struct

def cutoff(x):
    if x > 2**15-1:
        x = 2**15-1
    if x < -2**15:
        x = -2**15
    return x

Fs = 8000
# Try Fs = 16000 and 32000 

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients for second order #1
a1 = -1.8994 #values from matlab
a2 = 0.9971

# Difference equation coefficients for second order #2
a3 = -1.8999 #values from matlab
a4 = 0.9977

# Initialization
y1 = 0.0
y2 = 0.0
y1_1 = 0
y2_1 = 0
gain = 8000

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True, 
                frames_per_buffer = 1)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

#Cascading two second order difference equations

    #First difference equation 
    y0 = x0 - a1 * y1 - a2 * y2

    # Delays
    y2 = y1
    y1 = y0

    # Output after first filter
    out = y0

    #Second difference equation 
    y0_1 = out - a3 * y1_1 - a4 * y2_1

    y2_1 = y1_1
    y1_1 = y0_1

    # Output after second filter
    out_new = cutoff(gain * y0_1)

    str_out = struct.pack('h', out_new)     # 'h' for 16 bits
    stream.write(str_out, 1)

print("* done *")
stream.stop_stream()
stream.close()
p.terminate()

"""
Example program to demonstrate how to send time series to LSL
"""

import math, time

from pylsl import StreamInfo, StreamOutlet, local_clock

if __name__ == '__main__':
    # Sampling rate, on par with usual vsync framerate
    srate = 60
    # Identifier of the stream. Usually the name describe the device / model used, the type what data is being sent. Sticking with traditional examples values.
    lsl_name = 'BioSemi'
    lsl_type = 'EEG'

    # A stream info describe the meta data associated to the stream. We create two channels (x and y translations) of floats.
    # The last parameter is an ID that should be unique, used to automatically reconnect in case the stream is interrupted.
    info = StreamInfo(lsl_name, lsl_type, 2, srate, 'float32', 'myuid1337')

    # The outlet is the actual "pipe" outputing data, running in a separate thread
    outlet = StreamOutlet(info)

    print("now sending data...")
    # Infinity and beyond
    while True:
        # Prepare and send data
        mysample = [math.sin(local_clock()), math.cos(local_clock())]
        print(mysample)
        outlet.push_sample(mysample)
        # Wait before next push.
        # Note that relying on time.sleep to set the effective sampling rate (how many samples are sent per second) is sub-optimal, it will likely be slower and unstable
        # Check official LSL examples for a better way to steadily send data, e.g. compute how many samples are needed between two loops.
        time.sleep(1./srate)

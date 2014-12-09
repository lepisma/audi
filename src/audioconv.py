"""
Helper module with functions for interacting with data on audio port
"""

import pyaudio
import wave

def direct_play(file_name,
                sample_rate = 44100,
                chunk = 1024,
                channel = 1,
                width = 2):
    """
    Directly plays the data of the file without any keying or dac

    Parameters
    ----------
    file_name : str
        The name of file to be played
    sample_rate : int
        Sample rate to be assumed while playing. In data transfer,
        lower might help for less reception error
    chunk : int
        Chunk size to read file
    channel : int (1 or 2)
        1 for mono or 2 for stereo. 2 doesn't add anything for data
        transfer
    width : int
    """
    
    data_file = open(file_name, 'rb', chunk)

    # PyAudio instance
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format = p.get_format_from_width(width),
                    channels = channel,
                    rate = sample_rate,
                    output = True)

    data = data_file.read(chunk)

    # Playing the data
    while data != "":
        stream.write(data)
        data = data_file.read(chunk)

    # Ending things
    stream.stop_stream()
    stream.close()
    p.terminate()

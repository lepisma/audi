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

def direct_record(file_name,
                  time,
                  chunk = 1024,
                  sample_rate = 44100,
                  format = pyaudio.paInt16,
                  channel = 1):
    """
    Records the data coming from microphone and saves to the file specified.

    Parameters
    ----------
    file_name : str
        The name of the file to write data to
    time : int
        Recording time in seconds
    chunk : int
        The chunk size
    sample_rate : int
        The rate of signal sampling
    format
        The data format
    channel : int (1 or 2)
        1 (mono) or 2 (stereo)
    """

    p = pyaudio.PyAudio()

    stream = p.open(format = format,
                    channels = channel,
                    rate = sample_rate,
                    input = True,
                    frames_per_buffer = chunk)

    frames = []

    for i in range(0, int(sample_rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    data_file = open(file_name, 'wb', chunk)
    data_file.write(b''.join(frames))
    data_file.close()

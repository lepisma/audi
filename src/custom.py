"""
Custom cnversion of data to music
"""

import numpy as np
import pyaudio

def modulate(data):
    """
    Modulates the data given to be transferred via audi.
    
    Modulation works as described below
    - Change each uint8 element (byte) in the given array to
    binary representation
    - Form a wave byte by binning the 256 levels in 4 (higher might
    cause errors at receiving end)
    - So, each byte in wave is representing 2 bits of data.
    This gives (4 wave bytes) = (1 data byte)

    Neglecting the start and stop pattern, this should get to a
    speed of :
        sample_rate / (1024 * 4) KBps

    For (say) 18000Hz, speed = 4.39 KBps

    Parameters
    ----------
    data : numpy.ndarray
        Data array in numpy.uint8 format

    Returns
    -------
    wave : str
        The output in form of pulsating waves represented in a 
        form to work with pyaudio
    """

    wave = ''
    levels = ('\x00', '\x55', '\xaa', '\xff')
    
    for frame in data:
        next_num = frame
        for grp in range(4):
            wave += levels[next_num % 4]
            next_num /= 4

    return wave

def demodulate(wave):
    """
    Demodulates the data received from the microphone.

    Demodulation works as described below
    - Find the range of values
    - Scale the values (or don't, since the relative values are
    important)
    - Construct 2 bits per wave byte using the 4 levels
    - Construct the array of unit8 numbers

    Doing this on chunks rather than whole will allow the program
    to stop the stream after getting the stop pattern.

    Parameters
    ----------
    wave : str
        Wave from microphone

    Returns
    -------
    data : numpy.ndarray
        Data in numpy.uint8 array form
    """

    raw = np.frombuffer(wave, np.uint8)
    raw = np.array(raw, dtype = np.float16)
    max_data = np.max(raw) # Assuming it contains real '\xff'

    # Leveling data

    bins = np.linspace(0, max_data, 5)
    raw = np.digitize(raw, bins) - 1
    raw[raw == 4] = 3

    # Converting to base 10
    b4_conv_fact = [1, 4, 16, 64]
    raw = raw.reshape(raw.size / 4, 4)
    data = np.array(np.dot(raw, b4_conv_fact), dtype = np.uint8)
    
    return data

def add_trails(wave):
    """
    Adds start and stop pattern to the given wave
    
    Adding 'audi' on both sides
    """
    
    text = 'audi'
    as_int = map(ord, text)
    as_wave = modulate(as_int)

    return as_wave + wave + as_wave

def detect_start(data):
    """
    Detects if the data chunk has the start pattern in it

    Parameters
    ----------
    data : numpy.ndarray
        The data chunk returned by demodulator

    Returns
    -------
    has_start : boolean
        Tells if the chunk has start pattern
    position : int
        If the chunk contains the start pattern, it is the position
        of the first (relevant) data byte else it is -1
    """

    pass

def detect_end(data):
    """
    Detects if the chunk contains the end pattern

    Parameters
    ----------
    data : numpy.ndarray
        The data chunk returned by demodulator

    Returns
    -------
    has_end : boolean
        Tells if the chunk has end pattern
    position : int
        Position of last (relevant) data byte else -1
    """

    pass

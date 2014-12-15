"""
Tests for modulation and demodulation
"""

import unittest

import numpy as np
from ..src import custom

class TestModem(unittest.TestCase):

    def setUp(self):
        pass

    def test_length_modulation(self):
        """
        Test for the length of output for modulation
        """

        data = [221, 3, 42, 58]
        self.assertEqual(len(custom.modulate(data)), 4 * len(data))

    def test_length_demodulation(self):
        """
        Test for the length of output for demodulation
        """

        wave = '\x00\x55\xaa\xff\x00\x00\x00\x00'
        self.assertEqual(len(wave) / 4, len(custom.levels_to_data(custom.demodulate(wave))))

    def test_modulate(self):
        """
        Test for modulation correctness
        """

        data = np.array([187, 88, 255, 8])
        wave = '\xff\xaa\xff\xaa\x00\xaaUU\xff\xff\xff\xff\x00\xaa\x00\x00'
        outwave = custom.modulate(data)
        self.assertEqual(wave, outwave)

    def test_demodulate(self):
        """
        Test for demodulation correctness
        """

        wave = '\xff\xaa\xff\xaa\x00\xaaUU\xff\xff\xff\xff\x00\xaa\x00\x00'
        data = np.array([187, 88, 255, 8])
        outdata = custom.levels_to_data(custom.demodulate(wave))
        self.assertTrue(np.array_equal(data, outdata))
    
if __name__ == "__main__":
    unittest.main()
            

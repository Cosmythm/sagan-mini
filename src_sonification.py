# -*- coding: utf-8 -*-
"""src/sonification.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pJsxxiveqhXomCidWaV_kJlg_p4l2vwV
"""

import os
from astropy.io import fits
import numpy as np
import sounddevice as sd
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import torch

# Load Wav2Vec2 model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

# Path to the data directory
DATA_DIR = 'data/'

# Function to convert spectral data to sound
def spectrum_to_sound(wavelength, flux):
    # Normalize the flux to a range suitable for sound
    flux_normalized = (flux - np.min(flux)) / (np.max(flux) - np.min(flux))

    # Convert normalized flux to a sound wave
    duration = 1  # 1 second duration
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * 440 * flux_normalized * t)  # Simple sine wave

    return wave

# Function to process FITS files and generate sound
def process_spectrum(fits_file):
    with fits.open(fits_file) as hdul:
        data = hdul[1].data
        wavelength = data['wavelength']
        flux = data['flux']

        # Convert to sound
        sound_wave = spectrum_to_sound(wavelength, flux)
        sd.play(sound_wave, samplerate=44100)
        sd.wait()

# Main function to process all spectra in the data directory
def main():
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith('.fits'):
            print(f"Processing {file_name}")
            process_spectrum(os.path.join(DATA_DIR, file_name))

if __name__ == "__main__":
    main()
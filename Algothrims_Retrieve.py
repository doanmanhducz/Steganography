import numpy as np
import random as rd
import math
from scipy.io import wavfile
import pickle

def LSB(input_file, output_file, length):
    _, audio = wavfile.read(input_file)
    if audio.dtype == np.float32:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")

    least_bits = [byte & 1 for byte in audio[:(length*8)]]
    bytes = [least_bits[i:i+8] for i in range(0, len(least_bits), 8) if len(least_bits[i:i+8]) == 8]

    byte_arr = bytearray(int(''.join(map(str, byte)), 2) for byte in bytes)
    with open(output_file, 'wb') as file:
        file.write(byte_arr)


def PhaseCoding(input_file, output_file, length):
    _, audio = wavfile.read(input_file)
    if audio.dtype == np.float32:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")

    fft_audio = np.fft.fft(audio)
    message_bits = [0 if  np.abs(np.angle(fft_audio[i])) < float(math.pi/2) else 1 for i in range(length * 8) ]
    bytes = [message_bits[i:i+8] for i in range(0, len(message_bits), 8) if len(message_bits[i:i+8]) == 8]

    byte_arr = bytearray(int(''.join(map(str, byte)), 2) for byte in bytes)
    with open(output_file, 'wb') as file:
        file.write(byte_arr)


def SpredSpectrum(input_file, spread_code, output_file):
    _, audio = wavfile.read(input_file)
    if audio.dtype == np.float32:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")

    least_bits = [byte & 1 for byte in audio]
    least_bits = np.bitwise_xor(least_bits[:len(spread_code)], spread_code)
    bytes = [least_bits[i:i+8] for i in range(0, len(least_bits), 8) if len(least_bits[i:i+8]) == 8]

    byte_arr = bytearray(int(''.join(map(str, byte)), 2) for byte in bytes)
    with open(output_file, 'wb') as file:
        file.write(byte_arr)


with open('random_samples.pkl', 'rb') as pkl_file:
    spreads = pickle.load(pkl_file)

# length=1058752
# ext='.wav'

length=5000
ext='.txt'

LSB(input_file='audio_modified_LSB.wav', output_file=f'audio_retrieved_LSB{ext}', length=length)
PhaseCoding(input_file='audio_modified_PhCd.wav', output_file=f'audio_retrieved_PhCd{ext}', length=length)
SpredSpectrum(input_file='audio_modified_SS.wav', spread_code=spreads[4], output_file=f'audio_retrieved_SS{ext}')
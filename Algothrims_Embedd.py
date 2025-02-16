import numpy as np
import random as rd
import math
from scipy.io import wavfile
import pickle

def LSB(hiden_file, input_file, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]

    sample_rate, audio = wavfile.read(input_file)
    if audio.dtype == np.float32:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")

    if len(message_bits) > len(audio):
        raise SystemExit("The maximum message size can only be equal to the number of bytes in the file")
    else:
        print("Length of LSB:", len(message_bits))

    for index in range(len(message_bits)):
        least_bit = audio[index] & 1
        hiden_bit = message_bits[index]
        if least_bit != hiden_bit:
            audio[index] = audio[index] ^ 1

    if audio.dtype == np.float32:
        audio = audio.astype(np.float32) / 32767.0
    else:
        audio = audio.astype(np.int16)
    
    wavfile.write(output_file, sample_rate, audio)


def PhaseCoding(hiden_file, input_file, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]
    
    sample_rate, audio = wavfile.read(input_file)
    if audio.dtype == np.float32:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")

    if len(message_bits) > len(audio):
        raise ValueError("Message is too long to hide in audio.")
    else:
        print("Length of PhaseCoding:", len(message_bits))

    fft_audio = np.fft.fft(audio)
    for i in range(len(message_bits)):
        magnitude = np.abs(fft_audio[i])
        if message_bits[i] == 0:
            new_phase = 0
        else:
            new_phase = math.pi

        fft_audio[i] = magnitude * np.exp(1j * new_phase)
    
    modified_audio = np.fft.ifft(fft_audio).real
    if modified_audio.dtype == np.float32:
        modified_audio = modified_audio.astype(np.float32) / 32767.0
    else:
        modified_audio = modified_audio.astype(np.int16)
    
    wavfile.write(output_file, sample_rate, modified_audio)


def SpredSpectrum(hiden_file, input_file, spread_code, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]

    sample_rate, audio_data = wavfile.read(input_file)
    if audio_data.dtype == np.float32:
        audio_data = (audio_data * 32767).astype(np.int16)
    elif audio_data.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32")
    
    if len(message_bits) > len(spread_code):
        padding_size = len(message_bits) - len(spread_code)
        spread_code = np.pad(spread_code, (0, padding_size), mode='constant', constant_values=0)
    spread_message = np.bitwise_xor(message_bits, spread_code)

    if len(spread_message) > len(audio_data):
        raise SystemExit("The maximum message size can only be equal to the number of bytes in the file")
    else:
        print("Length of SpredSpectrum:", len(spread_message))

    for index in range(len(spread_message)):
        least_bit = audio_data[index] & 1
        hiden_bit = spread_message[index]
        if least_bit != hiden_bit:
            audio_data[index] = audio_data[index] ^ 1

    if audio_data.dtype == np.float32:
        audio_data = audio_data.astype(np.float32) / 32767.0
    else:
        audio_data = audio_data.astype(np.int16)
    
    wavfile.write(output_file, sample_rate, audio_data)


with open('random_samples.pkl', 'rb') as pkl_file:
    spreads = pickle.load(pkl_file)

hidden = 'hidden.txt'
# hidden = 'StarWars3.wav'
input = 'CantinaBand60.wav'

LSB(hiden_file=hidden, input_file=input, output_file='audio_modified_LSB.wav')
PhaseCoding(hiden_file=hidden, input_file=input, output_file='audio_modified_PhCd.wav')
SpredSpectrum(hiden_file=hidden, input_file=input, spread_code=spreads[4], output_file='Audio_modified_Teo.wav')
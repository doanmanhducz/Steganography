
import numpy as np
import random as rd
import math
import os
from scipy.io import wavfile
import pickle
import soundfile as sf

def prepare_spread_code(hiden_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]
    
    rd_sample_list = []
    for _ in range(10):
        rd_sample = np.random.randint(0, 2, size=(len(message_bits)))
        rd_sample_list.append(rd_sample.tolist())

    with open('random_samples.pkl', 'wb') as pkl_file:
        pickle.dump(rd_sample_list, pkl_file)

def LSB(hiden_file, input_file, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]

    # sample_rate, audio = wavfile.read(input_file)
    audio, sample_rate = sf.read(input_file)
    if audio.dtype == np.float32 or audio.dtype == np.float64:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32 or float64")

    if len(message_bits) > len(audio):
        raise SystemExit("The maximum message size can only be equal to the number of bytes in the file")

    for index in range(len(message_bits)):
        least_bit = audio[index] & 1
        hiden_bit = message_bits[index]
        if least_bit != hiden_bit:
            audio[index] = audio[index] ^ 1

    if audio.dtype == np.float32 or audio.dtype == np.float64:
        audio = audio.astype(np.float32) / 32767.0
    
    wavfile.write(output_file, sample_rate, audio)


def PhaseCoding(hiden_file, input_file, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [bit for byte in mgs_bytes for bit in format(byte, '08b')]
    
    # sample_rate, audio = wavfile.read(input_file)
    audio, sample_rate = sf.read(input_file)
    if audio.dtype == np.float32 or audio.dtype == np.float64:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32 or float64")

    num_bits = len(message_bits)
    num_samples = len(audio)

    if num_bits > num_samples:
        raise ValueError("Message is too long to hide in audio.")

    fft_audio = np.fft.fft(audio)
    for i in range(num_bits):
        magnitude = np.abs(fft_audio[i])
        if message_bits[i] == '0':
            new_phase = 0
        else:
            new_phase = math.pi

        fft_audio[i] = magnitude * np.exp(1j * new_phase)
    
    modified_audio = np.fft.ifft(fft_audio).real
    if audio.dtype == np.float32 or audio.dtype == np.float64:
        modified_audio = modified_audio.astype(np.float32) / 32767.0
    
    wavfile.write(output_file, sample_rate, modified_audio)


def SpreadSpectrum(hiden_file, input_file, spread_code, output_file):
    with open(hiden_file, 'rb') as file:
        mgs_bytes = file.read()
        message_bits = [int(bit) for byte in mgs_bytes for bit in format(byte, '08b')]

    # sample_rate, audio = wavfile.read(input_file)
    audio, sample_rate = sf.read(input_file)
    if audio.dtype == np.float32 or audio.dtype == np.float64:
        audio = (audio * 32767).astype(np.int16)
    elif audio.dtype != np.int16:
        raise SystemExit("Ensure the data type of the .wav file is int16 or float32 or float64")
    
    spread_message = np.bitwise_xor(message_bits, spread_code)

    if len(spread_message) > len(audio):
        raise SystemExit("The maximum message size can only be equal to the number of bytes in the file")

    for index in range(len(spread_message)):
        least_bit = audio[index] & 1
        hiden_bit = spread_message[index]
        if least_bit != hiden_bit:
            audio[index] = audio[index] ^ 1

    if audio.dtype == np.float32 or audio.dtype == np.float64:
        audio = audio.astype(np.float32) / 32767.0
    
    wavfile.write(output_file, sample_rate, audio)


if __name__ == '__main__':
    hidden = 'poem.txt'
    if not os.path.exists("random_samples.pkl"):
        print("Preparing spread code...")
        prepare_spread_code(hidden)

    with open('random_samples.pkl', 'rb') as pkl_file:
        spreads = pickle.load(pkl_file)

    input = [os.path.join(root, file) for root, dirs, files in os.walk("test-LibriSpeech") for file in files if file.endswith(".flac")]
    for inp in input:
        filename = os.path.basename(inp).replace(".flac", ".wav")
        LSB(hiden_file=hidden, input_file=inp, output_file=f"test-clean/LSB/LSB_{filename}")
        PhaseCoding(hiden_file=hidden, input_file=inp, output_file=f"test-clean/PhaseCoding/PhCd_{filename}")
        SpreadSpectrum(hiden_file=hidden, input_file=inp, spread_code=spreads[rd.randint(0, 9)], output_file=f"test-clean/SpreadSpectrum/SS_{filename}")
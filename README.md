# Steganography
## Introduction: Implementing Steganography in Text, Image, Audio, and Video.

This project combines the use of classical steganography techniques for concealing data with machine learning (ML) models to detect hidden information within audio and video files. The implemented steganography techniques include Least Significant Bit, Phase Coding, and Spread Spectrum, and the project allows for embedding various data types, including text, images, and audio.

Recently, numerous studies in this field have found that ML models can easily detect data that is intricately concealed using steganography techniques. Therefore, this project also provides a method by which a machine learning model can detect concealed data in audio by utilizing Convolutional Neural Networks (CNNs).

### Overview of the Algorithm Used: 
1. LSB (Least Significant Bit)
* Convert the hidden data (hidden.txt) into a bitstream.
* Read the .wav audio file and ensure the data type is either int16 or float32.
* Replace the least significant bit of each audio sample with the corresponding bit from the message.
* Save the modified audio file.<br>
![Image](https://github.com/user-attachments/assets/5eaea1c6-1b35-45e2-9786-facf90824742)<br>

2. Phase Coding
* Convert the message into a bitstream.
* Transform the audio file into the frequency domain using Fast Fourier Transform (FFT).
* Adjust the phase of the samples based on the message bits (0 → phase 0, 1 → phase π).
* Convert back to the time domain and save the modified file.<br>
![Image](https://github.com/user-attachments/assets/09dd44bf-e5ae-4f03-8260-b7e1b126d979)<br>

3. Spread Spectrum
* Convert the message into a bitstream.
* Read the audio file and convert it to int16 if necessary.
* Generate a spread spectrum code (spread_code) and XOR it with the message to distribute the hidden data across the entire audio signal.
* Replace the least significant bit of each audio sample with the XOR-ed hidden bit.
* Save the steganographed audio file.<br>
![Image](https://github.com/user-attachments/assets/664754d0-7fe1-4578-ad27-ecbc10a7f8c8)<br>

## Dataset
We use the original dataset, Acted Emotional Speech Dynamic Database [(data link)](https://m3c.web.auth.gr/research/aesdd-speech-emotion-recognition/), and process it with the `prepare_data.py` script to initialize the training and evaluation data for the CNN model.

## Enviroment
We conduct experiments with the ML model in the [Kaggle Notebook](https://www.kaggle.com/) environment, utilizing a Tesla P100 GPU with 16GB, 15GB of CPU, and 20GB of memory.

## Usage
### Using classical steganography techniques:
If you want to learn how to embed and retrieve various data types from audio files, run the `Algorithm_Embedd.py` and `Algorithm_Retrieve.py` scripts. Please note that the project currently only works with cover data in .wav file format.

### Using the ML model for steganalysis in audio:
If you want to learn how the ML model detects audio steganalysis, you can refer to the `steganography.ipynb` script. However, before you run the `steganography.ipynb` script, make sure you have prepared the data for training the model using the `prepare_data.py` script.





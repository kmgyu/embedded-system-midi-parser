# import numpy as np
from scipy.io.wavfile import write, read
import librosa
from pydub import AudioSegment

def mp3_to_wav(mp3_path, wav_path):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def wav_to_hz(file_path, time_interval):
    # Load the WAV file
    sample_rate, data = read(file_path)

    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Calculate the number of samples per interval
    samples_per_interval = int(sample_rate * time_interval)

    # Initialize a list to store the results
    hz_list = []

    # Process each interval
    for start in range(0, len(data), samples_per_interval):
        end = start + samples_per_interval
        segment = data[start:end]
        
        if len(segment) == 0:
            break
        
        # Perform Short-Time Fourier Transform (STFT)
        D = np.abs(librosa.stft(segment, n_fft=2048, hop_length=512))
        # if (D == 0).all(): print(D)
        # Extract the frequencies
        freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=2048)

        s = np.sum(D, axis=0)
        if not (s > 0).all(): s+=1

        # Calculate the mean frequency of the segment
        # 전부 0이면 zero division.
        mean_freq = np.max(np.dot(freqs, D) / s )
        
        hz_list.append(mean_freq)
    
    # Convert the list to a numpy array
    hz_array = np.array(hz_list)

    # Find the maximum frequency
    max_hz = np.max(hz_array)

    # Scale the frequencies to have a maximum of 1000 Hz
    if max_hz > 0:
        scale_factor = 1000 / max_hz
        hz_array = hz_array * scale_factor
    
    return hz_array


# # Example usage
# mp3_path = 'test.mp3'
# wav_path = 'test.wav'
# time_interval = 1.0  # 1 second intervals

# # Convert MP3 to WAV
# # mp3_to_wav(mp3_path, wav_path)

# # Analyze the WAV file
# hz_list = wav_to_hz(wav_path, time_interval)
# print(hz_list)

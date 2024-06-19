from wav_to_hz import *
from roboid import *

hamster = Hamster()

# interval : second
time_interval = 0.08  # 1 second intervals

file_name = "01. Ground Them"
wav_name = "test.wav"

mp3_to_wav(file_name+".mp3", "test.wav")
muse = wav_to_hz("test.wav", time_interval)

print(len(muse))

for hz in muse:
    print(hz)
    
    hamster.buzzer(hz)
    wait(time_interval*1000)
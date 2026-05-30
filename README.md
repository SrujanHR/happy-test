
# Happy — AI Voice Assistant

Happy is a personal AI voice assistant for Windows, built with Python. It listens for a wakeword, recognizes voice commands, speaks responses, and interacts with Google Gemini through Chrome automation.

This comprehensive document serves as the complete repository blueprint, containing the setup guide, configuration files, and application source code.


## 1. Project Overview & Features

- **Wakeword Detection**: Continuous low-overhead listening powered by Vosk.
- **Speech Recognition**: High-accuracy command processing via Google SpeechRecognition API.
- **Text-to-Speech (TTS)**: Natural voice synthesis using gTTS with seamless VLC media playback.
- **Gemini Integration**: Dynamic browser automation via Chrome to query Google Gemini.
- **State Management**: Automated persistence for active session runtimes and volume levels.


## 2. System Requirements

- **OS**: Windows 10 or 11
- **Python**: Version 3.10 or higher
- **Applications**: Google Chrome, VLC Media Player (64-bit standard installation)
- **Acoustic Model**: Vosk English model (e.g., `vosk-model-en-in-0.5` extracted into the `models/` directory)


## 3. Repository Files

### `requirements.txt`
```text
vosk
pyaudio
SpeechRecognition
pyautogui
pyperclip
clipboard
python-vlc
gTTS
soundfile
numpy
```


### `.gitignore`

```text
__pycache__/
venv/
*.pyc
combined_audio.wav
audio_*.wav
runtime.txt
current_vol.txt
.DS_Store

```

### `runtime.txt`

```text
0

```

### `current_vol.txt`

```text
50

```

### `src/happy.py`

```python
"""Happy — Voice Assistant entrypoint.

Update MODEL_PATH, CHROME_PATH, and VLC_LIB_DIR to match your system paths.
"""
import os
import time
import subprocess
import sys

# === VLC Path Binding Configuration ===
# Forces Windows environment paths to discover local VLC binaries
VLC_LIB_DIR = r"C:\Program Files\VideoLAN\VLC"
if os.path.exists(VLC_LIB_DIR) and VLC_LIB_DIR not in os.environ['PATH']:
    os.environ['PATH'] = VLC_LIB_DIR + os.pathsep + os.environ['PATH']

from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition as sr
import pyautogui
import pyperclip
import clipboard
from gtts import gTTS
import soundfile as sf
import numpy as np
import vlc

# === Configuration (edit to your machine) ===
MODEL_PATH = os.path.join('models', 'vosk-model-en-in-0.5')
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL_GEMINI = "[https://gemini.google.com/app](https://gemini.google.com/app)"
WAKEWORD = "happy"

# === Runtime files ===
RUNTIME_FILE = 'runtime.txt'
VOLUME_FILE = 'current_vol.txt'
for f, default in [(RUNTIME_FILE, '0'), (VOLUME_FILE, '50')]:
    if not os.path.exists(f):
        with open(f, 'w') as fh:
            fh.write(default)

# === Load Vosk model ===
if not os.path.exists(MODEL_PATH):
    print(f"Warning: Vosk model not found at {MODEL_PATH}. Please download and place it correctly.")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000)

def play_audio_clip(path):
    instance = vlc.Instance('--no-video')
    player = instance.media_player_new()
    player.set_media(instance.media_new(path))
    player.play()
    time.sleep(0.2) # Brief calibration buffer
    while player.get_state() not in [vlc.State.Ended, vlc.State.Error]:
        time.sleep(0.05)

def speak_text(text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    for i, s in enumerate(sentences):
        file_path = f'audio_{i}.wav'
        gTTS(text=s, lang='en', slow=False).save(file_path)
        play_audio_clip(file_path)
        try:
            os.remove(file_path)
        except OSError:
            pass

# === Wakeword loop ===
def vosk_recognize():
    print('Listening for wakeword...')
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                res = rec.Result().lower()
                if WAKEWORD in res:
                    print('Wakeword detected')
                    recognize_and_process()
                elif 'quit' in res:
                    break
    except KeyboardInterrupt:
        print('Stopped by user')
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

# === Command processing ===
def recognize_and_process():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        if os.path.exists('notify.wav'):
            play_audio_clip('notify.wav')
        try:
            audio = r.listen(src, timeout=3, phrase_time_limit=6)
            text = r.recognize_google(audio)
            print('You said:', text)
        except Exception:
            print("Listening failed or timed out.")
            return

    try:
        subprocess.Popen([CHROME_PATH, URL_GEMINI])
        time.sleep(4) # Allow window rendering overhead
        pyautogui.click(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)
        pyautogui.write(text, interval=0.01)
        pyautogui.press('enter')
    except Exception as e:
        print(f"Automation sequence failed: {e}")

if __name__ == '__main__':
    vosk_recognize()

```


## 4. Installation & Deployment Steps

1. **Clone & Navigate:**
```bash
git clone [https://github.com/](https://github.com/)<your-username>/happy-assistant.git
cd happy-assistant

```


2. **Initialize Environment:**
```bash
python -m venv venv
.\venv\Scripts\activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


*Note: If pyaudio compilation fails on your Windows environment, install it via pre-compiled wheels:*
```bash
pip install pipwin
pipwin install pyaudio

```


4. **Execution:**
```bash
python -m src.happy

```




## 5. License

This project is licensed under the MIT License.

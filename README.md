
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
[Set this to 0 the program will update this as you keep using it.]
This is the gTTS usage counter to make sure you don't cross your free usage limit.
Eg:
0
```

### `current_vol.txt`

```text
[Set this to your current system voice level the program will update this as you keep using it.]
Eg:
50

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

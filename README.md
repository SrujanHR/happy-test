
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


## 4. Installation & Deployment Steps
0. **Make sure you have git installed** 
Git is not the same as GitHub.
you can install git from here : https://git-scm.com/install/
I DO NOT recommend using the latest Python versions as some dependencies take time to integrate them into their workflow NOTE I am talking about the 3.XX not the 3.00.XX
1. **Clone & Navigate:**
```bash
git clone [https://github.com/](https://github.com/)<your-username>/happy-assistant.git
cd Happy-AI-Voice-Assistant-main

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
4. **Install VOSK model**
https://alphacephei.com/vosk/models
I have used the "vosk-model-en-in-0.5"
download the .zip and extract into the root folder

5. **Repository Files That need to be updated**
      
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
     ### `Happy_AI.py`
       chrome_path = r""  # Update the path to your Chrome installation
       usually: C:\Program Files\Google\Chrome\Application\chrome.exe

7. **Execution:**
```bash
python -m "Bard assistant.py"

```




## 5. License

This project is licensed under the MIT License.

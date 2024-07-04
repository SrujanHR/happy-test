
import pyautogui,time,pyperclip,subprocess,clipboard#,pyttsx4
pyautogui.FAILSAFE =False

from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition as sr
import webbrowser
import time
import pyautogui
import clipboard
import os
import subprocess



import vlc
from gtts import gTTS
import concurrent.futures
import soundfile as sf
import numpy as np


import threading

#inp= text#input("enter your qustion : ")
time1 = 0.1
x,y=pyautogui.size()
#print(x,y)
x = x//2.34
y = y //1.134
#print(x,y)
'''engine = pyttsx4.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)'''
url = "https://gemini.google.com/app"


# Load the Vosk acoustic model
model =Model(r"vosk-model-en-in-0.5")

# Create a KaldiRecognizer object
rec = KaldiRecognizer(model, 16000)

# Define the wakeword to detect
global wakeword
wakeword = "happy"

# Open an audio stream using PyAudio
global p
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=16000)

# Main loop for real-time wakeword detection
print("Listening for wakeword...")
def generate_audio(sentence, index):
    audio = gTTS(sentence, lang='en', slow=False)
    audio.save(f'audio_{index}.mp3')

def play_audio_clip(file_path):
    instance = vlc.Instance('--no-video')  # Create a new instance without video support
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()
    while player.get_state() != vlc.State.Ended:
        continue
    player.release()

def combine_audio_files(input_sentence):
    name_of_file = []
    sentences = [s.strip() for s in input_sentence.split('.') if s.strip()]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, sentence in enumerate(sentences):
            executor.submit(generate_audio, sentence, i)

    for k in range(len(sentences)):
        name_of_file.append(f'audio_{k}.mp3')

    audio_files = name_of_file
    combined_data = np.array([])

    for audio_file in audio_files:
        data, samplerate = sf.read(audio_file)
        combined_data = np.concatenate((combined_data, data))

    combined_path = "combined_audio.wav"
    sf.write(combined_path, combined_data, samplerate)

    for i in range(len(sentences)):
        file_path = f'audio_{i}.mp3'
        if os.path.exists(file_path):
            os.remove(file_path)

    play_audio_clip('combined_audio.wav')

def vosk_recognize():
    global data, result  # Declare global variables
    while True:
        data = stream.read(16000)  # Read audio data from the stream
        print("Listening for wakeword...")
        if len(data) == 0:
            return
        if rec.AcceptWaveform(data):
            result = rec.Result()
            if wakeword in result:
                print("Wakeword detected!")
                
                '''media_player = vlc.MediaPlayer()
                media_player.set_media(vlc.Media("notify.wav"))
                media_player.audio_set_volume(100)
                media_player.play()'''
                # Trigger desired action or command here
                speecch_recognition()
                # chat_gpt_it()
            elif 'quit' in result:
                exit()
        else:
            result = rec.PartialResult()


def speecch_recognition():
    global input_gpt
    input_gpt = 0
    global content_file_name
    content_file_name = 0
    global title_file_path
    title_file_path = 0
    global listToStr
    listToStr = 0
    global engine
    '''engine = pyttsx4.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)'''

    # Create a recognizer instance
    global recognizer
    recognizer = sr.Recognizer()

    # Load previous runtime from file
    with open('runtime.txt', 'r') as f:#C:/Users/Srujan/Desktop/assistant/New folder/runtime.txt', 'r') as f:
        previous_runtime = float(f.read())

    # Check if time limit is reached
    if previous_runtime <= 3000:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            play_audio_clip(r'notify.wav')
            print("Speak something...")
            start_time = time.time()
            global audio_data
            audio_data = recognizer.listen(source,phrase_time_limit=5)  # Listen for audio input with a maximum duration of 5 seconds
            if audio_data:
                try:
                    global text
                    text = recognizer.recognize_google(audio_data)  # Use Google Speech Recognition API
                    print("Recognized text: ", text)
                except sr.UnknownValueError:
                    pass
                    #vosk_recognize()
                except sr.RequestError as e:
                    vosk_recognize()
                except Exception as e:
                    vosk_recognize()
            else:
                vosk_recognize()

            # Calculate the current runtime by subtracting the previous runtime from the current time
            current_runtime = time.time() - start_time + previous_runtime

            # Write the current runtime to the file
            with open('runtime.txt', 'w') as f:
                f.write(str(current_runtime))

            # Calculate the total time used in a month (3000 seconds)
            total_time_used = min(current_runtime, 3000)

    else:
        print('Time limit reached')
    Bard_It()

def increase_vol(j):
    f = open("current_vol.txt", "w")
    for i in range(j):
        pyautogui.press("volumeup")
        time.sleep(0.2)
    k = vol + (j * 2)
    f.write(str(k))
    f.close()

def decrease_vol(j):
    f = open("current_vol.txt", "w")
    for i in range(j):
        pyautogui.press("volumedown")
        time.sleep(0.2)
    k = vol - (j * 2)
    f.write(str(k))
    f.close()
# Use the 'chrome' command to open a new window in Chrome
def Bard_It():
    global inp
    inp= text#input("enter your qustion : ")
    if 'good morning' in inp:
        inp ='think of yourself as jarvis but dont say it, and answer this in a witty way : tell me good morining about todays weather,possibility of rain , special occasion if any ,and ask me if i would like to LISTEN TO A song,'
    if 'weather' in inp:
        inp +=  ' in mysuru with degree in  celsius'
    elif 'play' in inp:
        #input_thread()\
        input_thread = threading.Thread(target=search_and_play_song(inp))
        input_thread.start()
        return
    elif 'turn on' in inp:
        pass
    elif 'turn off' in inp:
        pass
    elif 'pause' in inp:
        print('pause', running)
        if running == 'local song' and player is not None:
            player.pause()
            print('pausing song')
        elif running == 'youtube':
            print('pausing YT')
            partial_title = 'Google'
            switch_to_window_play(partial_title)
        return
    elif 'continue' in inp or 'resume' in inp:
        if running == 'local song' and player is not None:
            player.play()
        if running == 'youtube':
            print('pausing YT')
            partial_title = 'Google'
            switch_to_window_play(partial_title)
        return
    elif 'stop' in inp:
        if running == 'local song' and player is not None:
            player.stop()
        if running == 'youtube':
            clipboard.copy('The attribute value is equal to "Replay"')
            time.sleep(1)
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running = False
            vosk_recognize()
        return
    if 'volume' in inp:
        global vol , a ,f
        a = inp
        f = open("current_vol.txt", "r")

        vol = int(f.read())
        if 'volume' in a:
            a = a.replace("volume", "")
        if 'set' in a:
            a = a.replace("set", "")
        if 'by'in a:
            a = a.replace("by", "")
        if 'to'in a:
            a = a.replace("to", "")
        elif "increase" in a and 'volume'in a :
            a = a.replace("increase", "")
            a = a.replace("volume", "")
            j = int(int(a) / 2)
            increase_vol(j)
            return
        # Handle decrementing volume
        elif "decrease" in a and 'volume'in a:
            a = a.replace("decrease", "")
            a = a.replace("volume", "")
            j = int(int(a) / 2)
            decrease_vol(j)
            return
        # Handle setting volume
        else:
            a = int(a)
            if 100 > a > vol:
                j = int((a - vol) / 2)
                increase_vol(j)

            elif 0 < a < vol:
                j = int((vol - a) / 2)
                decrease_vol(j)
            return
    '''elif 'news' in inp:
        inp+=' from mysuru , india and karnataka'''
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update the path to your Chrome installation
    subprocess.Popen([chrome_path, url])
    time.sleep(4)
    pyautogui.moveTo(x,y)
    pyautogui.click()
    pyautogui.write(inp)
    time.sleep(1)
    pyautogui.press('Enter')
    Retrive_It1(time1)
def Retrive_It1(time1):
    time.sleep(time1)
    pyautogui.press('F12')
    time.sleep(0.3)
    pyautogui.moveTo(1400,700)
    time.sleep(0.5)
    pyautogui.click()
    Retrive_It2()
def Retrive_It2():
    long_essay = r"""
    // Get all elements with the class "markdown"
    const markdownElements = document.getElementsByClassName('markdown');

    // Loop through each element and print its text content
    for (let i = 0; i < markdownElements.length; i++) {
      const element = markdownElements[i];
      const text = element.textContent;
      //console.log(text);
      copy(text)
    }"""

    time.sleep(1)
    clipboard.copy(long_essay)
    # Type the long essay in Notepad
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('Enter')
    clipboard_content = pyperclip.paste()
    if  clipboard_content == long_essay:
        Retrive_It2()
        
    else:
        speak()
        pass

def speak():
    #clipboard_content = pyperclip.paste()
    clipboard_content = pyperclip.paste()
    if ' Use code with caution. Learn morecontent_copyHere is another one:Code snippet'in clipboard_content:
        clipboard_content.replace(' Use code with caution. Learn morecontent_copyHere is another one:Code snippet','')
    elif 'Code snippet'in clipboard_content:
        clipboard_content.replace('Code snippet','')
    #if clipboard_content:
    my_variable = clipboard_content
    print(my_variable)
    combine_audio_files(my_variable)
    '''engine.say(my_variable)
    engine.runAndWait()
    time.sleep(1)'''
    subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#music


folder_path = r'D:/Srujan Drive/Mobile/music'  # Specify the folder path to search in
file_exts = [".mp4", ".m4a"]  # Specify the file extensions to search for
running = False
player = None


def switch_to_window(partial_title):
    #import pyautogui,time
    c = 0
    while partial_title not in  pyautogui.getActiveWindowTitle() :
            pyautogui.keyDown('alt')
            for i in range(c):
                
                pyautogui.press('tab')
            pyautogui.keyUp('alt')
            c+=1



def Open_Chrome_For_Youtube(time2):
    time.sleep(time2)
    pyautogui.hotkey('ctrl', 'shift', 'i')  # Open the Developer Tools (Chrome shortcut)
    time.sleep(0.3)  # Wait for the Developer Tools to open
    pyautogui.hotkey('ctrl', '`')  # Toggle the console tab (Chrome shortcut)

    time.sleep(1)
    pyautogui.moveTo(1500, 970)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(0.3)
    
    time.sleep(time2)
    global long_essay
    long_essay = r"""
    // Select the element by its class name
    const button = document.querySelector('.ytp-play-button');

    // Get the attribute value
    const dataTitleNoTooltip = button.getAttribute('data-title-no-tooltip');

    // Check if the attribute value is equal to 'Replay'
    if (dataTitleNoTooltip === 'Replay') {
      // Code to execute if the condition is true
      const message = 'The attribute value is equal to "Replay"';
      console.log(message);
      copyToClipboard(message);
    } else {
      // Code to execute if the condition is false
      console.log('The attribute value is not equal to "Replay"');
    }

    // Function to copy text to clipboard
    function copyToClipboard(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
    """

    time.sleep(1)
    clipboard.copy(long_essay)
    Browse_For_The_Song(time2)

def Browse_For_The_Song(time2):

    # Type the long essay in Notepad
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('Enter')
    clipboard_content = pyperclip.paste()
    #threading.Thread(target=Check_if_YT_Video_Stopped, args=(clipboard_content,)).start()
    time.sleep(1)
    if clipboard_content == long_essay:
        Browse_For_The_Song(1)
        #Check_if_YT_Video_Stopped(clipboard_content, time2)
    elif clipboard_content == 'The attribute value is equal to "Replay"':
        print('finished playing')
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running = False
    else:
        pass



'''def switch_to_window_pause(partial_title):

    c = 0
    while partial_title not in  pyautogui.getActiveWindowTitle() :
            pyautogui.keyDown('alt')
            for i in range(c):
                
                pyautogui.press('tab')
            pyautogui.keyUp('alt')
            c+=1


    # Pause the YouTube video
    pyautogui.moveTo(400, 500)
    pyautogui.click()
    #time.sleep(0.5)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(1050, 980)
    pyautogui.click()'''



def switch_to_window_play(partial_title):
    #import pyautogui,time
    c = 0
    while partial_title not in  pyautogui.getActiveWindowTitle() :
            pyautogui.keyDown('alt')
            for i in range(c):
                
                pyautogui.press('tab')
            pyautogui.keyUp('alt')
            c+=1
    

    # Play the YouTube video
    pyautogui.moveTo(400, 500)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(1500, 980)
    pyautogui.click()



def search_and_play_song(inp):
    global running, player

    def search_file(folder, filename):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if filename.lower() in file.lower():
                    return os.path.join(root, file)
        return None

    if 'play' in inp:
        if running == 'youtube':
            partial_title = 'Google'
            switch_to_window_play(partial_title)
        elif running != 'youtube':
            running = 'local song'
            inp = inp.replace('play ', '')
            print(inp)
            input_name = inp

            found_files = []

            for ext in file_exts:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if input_name.lower() in file.lower() and file.lower().endswith(ext):
                            found_files.append(os.path.join(root, file))

            if found_files:
                print("Files found:")
                for file in found_files:
                    print(file)
                vlc_path = r'C:\Program Files\VideoLAN\VLC\libvlc.dll'
                os.add_dll_directory(vlc_path)
                music_file = found_files[0]
                player = vlc.MediaPlayer(music_file)
                player.play()
                running = 'local song'
            else:
                print("No files found.")
                if running == 'local song' and player is not None:
                    player.pause()
                    print('pausing song')
                else:
                    pass
                running = 'youtube'
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                url = "https://www.youtube.com/"
                subprocess.Popen([chrome_path, url])
                time.sleep(4)
                pyautogui.moveTo(800, 100)
                pyautogui.click()
                time.sleep(1)
                pyautogui.write(inp)
                pyautogui.press('enter')
                time.sleep(2)
                pyautogui.moveTo(800, 300)
                pyautogui.click()
                global time2
                time2 = 1
                threading.Thread(target=Open_Chrome_For_Youtube, args=(time2,)).start()

    
        
def input_thread():
        #while True:
        #inp =text# input("Enter your question: ")  # Get user input
        # Create and start the input thread

        search_and_play_song(inp)




vosk_recognize()





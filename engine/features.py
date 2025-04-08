# from playsound import playsound
import eel
import os
import webbrowser
from pygame import mixer
from engine.config import ASSISTANT_NAME
from engine.command import *
import pywhatkit as kit
import re 
import sqlite3
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import extract_yt_term
from urllib.parse import quote
import subprocess
from engine.helper import remove_words
import pyautogui
# from hugchat import hugchat
import google.generativeai as genai
import os

conn = sqlite3.connect("EchoSphear.db")
cursor = conn.cursor()

# # Playing assistant sound function
@eel.expose
def playAssistantsound():
    music_dir = r"www\assets\audio\start_sound.mp3"
    mixer.init()
    mixer.music.load(music_dir)
    mixer.music.play()


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))

                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except Exception as e:
            speak(f"Something went wrong: {e}")
            print(f"Error: {e}")
    
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("playing" + search_term + "on YouTube")
    kit.playonyt(search_term)
    

#-----------------------------------------------------------------------------------------------------------

# from pytube import YouTube
# def DownloadYoutube(query):
#     search_term = extract_yt_term(query)
#     if search_term:
#         speak("Downloading " + search_term + " from YouTube")
#         url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
#         yt = YouTube(url)
#         video = yt.streams.get_highest_resolution()
#         video.download("C:\\Users\\darsh\\Videos\\echoSphear")  # Specify the download path
#         speak("Download complete")

#-----------------------------------------------------------------------------------------------------------


def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        
        # Replace 'YOUR_ACCESS_KEY' with your actual access key
        access_key = "bt6Nlo8P44kTKDoljvDbFEZchHdy5n2cS6W708K6VpX9nVX4cfpH1Q=="
        keyword_paths = r".\\hey-sphear_en_windows_v3_0_0.ppn"
        porcupine = pvporcupine.create(
            access_key=access_key, 
            keyword_paths=[keyword_paths], 
            keywords=[keyword_paths,"jarvis","alexa"]
        )

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,  # Fixed typo
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        print("Listening for hotwords...")

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)  # Fixed typo

            if keyword_index >= 0:
                print("Hotword detected!")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    words_to_remove = ['make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()
    
    print(f"[DEBUG] Processed Query: '{query}'")  # Debugging

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        if not results:
            print("[DEBUG] Contact not found in database.")
            speak("Contact not found.")
            return 0, 0

        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        print(f"[DEBUG] Found Contact: {query}, Mobile: {mobile_number_str}")
        return mobile_number_str, query

    except Exception as e:
        print(f"[ERROR] Error in findContact: {e}")
        speak('Error retrieving contact.')
        return 0, 0

def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
 
         jarvis_message = "Message sent successfully to " + name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to " + name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+ name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
    time.sleep(5)

    if flag == 'message':
        pyautogui.hotkey('enter')

    speak(jarvis_message)

    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot
# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response = chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response

# import google.generativeai as genai

def chatBot(query):
    user_input = query.lower()

    try:
        # Configure Gemini API key
        genai.configure(api_key="AIzaSyBafI6ozxGzlisQxPITBs_vjKRxgI6ZwYs")

        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-pro-latest') #gemini-1.5-flash

        # Generate a response using the Gemini model
        response = model.generate_content(user_input)

        # Check if response is valid
        if response and response.text:
            reply = response.text
        else:
            reply = "Sorry, I couldn't generate a response."

    except Exception as e:
        reply = f"An error occurred: {str(e)}"

    # Print and optionally speak the response
    print(reply)
    speak(reply)

    return reply

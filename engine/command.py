import pyttsx3
import speech_recognition as sr
import eel
import time
import threading


engine = None  # Global engine
engine_lock = threading.Lock()

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()



def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        # time.sleep(2)
        
    except Exception as e:
        print("Sorry, I couldn't understand. Please repeat.")
        return "Sorry"
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1 :
        query = takecommand()
        print(f"[DEBUG] Recognized Query: {query}")
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        

        if "open" in query:
            from engine.features import openCommand
            print("[DEBUG] Executing openCommand")
            openCommand(query)
        
        elif "on youtube" in query or "in youtube" in query:
            from engine.features import PlayYoutube
            print("[DEBUG] Executing PlayYoutube")
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            
            print("[DEBUG] Searching for contact...")
            flag = ""
            contact_no, name = findContact(query)
            
            if contact_no != 0:
                if "send message" in query:
                    speak("What message should I send?")
                    query = takecommand()
                    if not query:
                        print("[DEBUG] No message received, cancelling operation.")
                        speak("Message not received. Cancelling operation.")
                        return
                    flag = 'message'
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                
                print(f"[DEBUG] Contact Found: {name}, Number: {contact_no}, Action: {flag}")
                whatsApp(contact_no, query, flag, name)
            else:
                print("[DEBUG] Contact not found.")
                speak("Contact not found.")
        
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
    
    eel.ShowHood()  

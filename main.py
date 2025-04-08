import os
import eel
from engine.features import *
from engine.command import *



def start():
    eel.init("www")

    playAssistantsound()
    # os.system('start chrome --app="http://localhost:8000/index.html" ')
    # os.system('start firefox --kiosk "http://localhost:8000/index.html"')
    os.system('start msedge --app="http://localhost:8000/index.html"')

    eel.start("index.html",mode=None,host="localhost",block=True)
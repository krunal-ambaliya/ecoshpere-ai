import multiprocessing

def start():
    print("Process 1 is running.")
    from main import start
    start()

def listenHotword():
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=start)  # Corrected
    p2 = multiprocessing.Process(target=listenHotword)  # Corrected

    p1.start()
    p2.start()

    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()


    print("System stopped.")

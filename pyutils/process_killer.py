import os
import signal

def kill_process(message):

    try:
        pid = int(message.split(" ")[1])
        os.kill(pid, signal.SIGKILL)
        return f"Process with PID {pid} killed successfully."
    except ProcessLookupError:
        return f"No process with PID {pid} found."
    except PermissionError:
        return f"Permission error. Unable to kill process with PID {pid}."
    except Exception as e:
        return e
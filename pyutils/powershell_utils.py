
import subprocess

def powershell(message: str):
    cmd = message[11:]
    pshell = f"%systemroot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
    response = subprocess.Popen(f"{pshell} {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = response.communicate()
    if error: response = error.decode()
    else: response = output.decode()
    return response

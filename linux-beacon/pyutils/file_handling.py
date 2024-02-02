import os

def handle_cd(message):
    try:
        os.chdir(message[3:])
        return os.getcwd()
    except Exception as e: return f"Error in handle_cd(): {e}"

def handle_mkdir(message):
    try:
        os.mkdir(message[6:])
        dirl = os.listdir()
        dirl[dirl.index(message[6:])] = f"\033[31;1m{dirl[dirl.index(message[6:])]}\033[0m"
        return "\n".join(dirl)
    except:
        return f"Successfully created {message[6:]}"
    
def listdir_handler(_):
    try: return "\n".join(os.listdir())
    except Exception as e: return f"Error in listdir_handler: {e}"

def pwd(_):
    try: return os.getcwd()
    except Exception as e: return f"Error in pwd(): {e}"

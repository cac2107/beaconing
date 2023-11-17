import os

def handle_cd(message):
    try:
        os.chdir(message[3:])
        return os.getcwd()
    except Exception as e:
        return e

def handle_mkdir(message):
    os.mkdir(message[6:])
    dirl = os.listdir()
    try:
        dirl[dirl.index(message[6:])] = f"\033[31;1m{dirl[dirl.index(message[6:])]}\033[0m"
        return "\n".join(dirl)
    except:
        return f"Successfully created {message[6:]}"
    
def listdir_handler(_): return "\n".join(os.listdir())

def pwd(_): return os.getcwd()

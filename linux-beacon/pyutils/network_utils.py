import socket
import threading
import time

def port_helper(l: list, i: int):
    try:
        host = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, i))
        l.append(str(i))
    except: pass

def scan_ports(message):
    try:
        ports = message[11:].split(" ")
        open_ports = []
        maxi = int(ports[1])
        for i in range(int(ports[0]), maxi):
            t = threading.Thread(target=port_helper, args=[open_ports, i])
            t.start()
        time.sleep(1)
        return ", ".join(open_ports)
    except Exception as e: return f"Error in scan_ports: {e}"

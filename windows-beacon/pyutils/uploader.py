import requests

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
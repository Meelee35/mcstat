import requests

from mcstat.log import vprint, warn, fatal

def _validate(data: dict):
    if "online" not in data:
        fatal("Unknown server.")

    online = data.get("online")
    ip = data.get("ip_address")

    if ip is None:
        fatal("Invalid or unknown server address.")

    if not online:
        fatal("Server is not online.")

def get_data(url: str) -> dict:
    print("Fetching...")
    vprint("Fetching from url: " + url)
    
    response = requests.get(url)
    if response.status_code == 400 and "Invalid address value" in response.text:
        fatal("Invalid or unknown server address.")

    try:
        response.raise_for_status()

        data = response.json()

        _validate(data)
        print("Done!\n")
        return data

    except Exception as e:
        fatal(e, " while fetching data.")

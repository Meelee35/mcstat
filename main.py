import argparse
import requests
import sys
from typing import NoReturn

from PIL import Image
import base64
import io

VERSION = "1.1"

verbose = False

# IconRenderer class
# Now using classes to make coding easier
class IconRenderer:
    def __init__(self, size: int = 16):
        self.size = size

    def render(self, data: dict) -> None:
        icon = data.get("icon")

        if not icon:
            fatal("No icon provided")

        img_bytes = self._extract_bytes(icon)
        self._draw(img_bytes)

    def _extract_bytes(self, icon: str) -> bytes:
        if "," in icon:
            icon = icon.split(",", 1)[1]

        return base64.b64decode(icon)

    def _draw(self, img_bytes: bytes) -> None:
        img = Image.open(io.BytesIO(img_bytes))
        img = img.convert("RGBA")
        img = img.resize((self.size, self.size), Image.NEAREST)

        pixels = img.load()

        print()

        for y in range(self.size):
            line = ""

            for x in range(self.size):
                r, g, b, a = pixels[x, y]

                if a < 128:
                    pixel = " "
                else:
                    pixel = self._block(r, g, b)
                line += pixel * 2

            print(line)

        print()

    def _block(self, r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m \033[0m"


def vhint() -> None:
    if not verbose:
        print("Use verbose mode for extra info. (-v)")

def vprint(*args, **kwargs) -> None:
    if verbose:
        print(*args, **kwargs)


def fatal(e:Exception | str, doing: str | None = None) -> NoReturn:
    name = e if isinstance(e, str) else type(e).__name__
    msg = f"{doing}" if doing else ""
    print(f"\033[31mFatal: {name} {msg}\033[0m")

    if isinstance(e, Exception):
        vhint()
        vprint(e)

    sys.exit(1)

def warn(e: Exception | str, doing: str | None = None) -> None:
    name = e if isinstance(e, str) else type(e).__name__
    msg = f"{doing}" if doing else ""
    print(f"\033[33mWarning: {name} {msg}\033[0m")

    if isinstance(e, Exception):
        vhint()
        vprint(e)

# api url constructor
def api_url(host: str, port: int): 
    return f"https://api.mcstatus.io/v2/status/java/{host}:{port}"

# Argument parser
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Server IP or hostname")
    parser.add_argument("port", nargs="?", type=int, default=25565, help="Server port (Default: 25565)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-i", "--icon", nargs="?", const=16, type=int, metavar="SIZE", help="Display server's icon instead of standard information (Default: 16px)")
    return parser.parse_args()

# Fetch data
def get_data(url: str) -> dict:
    print("Fetching...")
    vprint("Fetching from url: " + url)
    
    response = requests.get(url)
    if response.status_code == 400 and "Invalid address value" in response.text:
        fatal("Invalid or unknown server address.")

    try:
        response.raise_for_status()

        print("Done!\n")
        return response.json()

    except Exception as e:
        fatal(e, " while fetching data.")

# Display MOTD
def display_motd(data: dict) -> None:
    motd_dict = data.get("motd")

    if motd_dict:
        motd = motd_dict["clean"]
        
        for line in motd.splitlines():
            print(line.strip())
        print()
    else:
        warn("No MOTD available.")

# Display version
def display_version(data: dict) -> None:
    version_dict = data.get("version")
    vprint(version_dict)

    if version_dict:
        print(f"Version: {version_dict['name_clean']}")
    else:
        warn("No version information provided")

# Display players
def display_players(data: dict) -> None:
    players_dict = data.get("players")
    vprint(f"Players dict: {players_dict}")
    
    if players_dict:
        online = players_dict["online"]
        max_players = players_dict["max"]
        player_list = players_dict["list"]
        
        print(f"Players: {online} / {max_players}")

        if online > 0:
            print(f"Players: {', '.join(player['name_clean'] for player in player_list)}" if player_list else "No player list available")
        
    else:
        warn("No player info provided.")


# Display handler
def display_data(data: dict, render_icon: bool, icon_size: int = 16) -> None:
    vprint("Displaying server data")

    if "online" not in data:
        fatal("Unknown server.")

    online = data.get("online")
    ip = data.get("ip_address")

    if ip is None:
        fatal("Invalid or unknown server address.")

    if not online:
        fatal("Server is not online.")

    if render_icon:
        vprint("Rendering icon")
        icon_renderer = IconRenderer(size=icon_size)
        icon_renderer.render(data)
        return
    vprint("Not rendering icon")
    
    display_motd(data)
    display_version(data)
    display_players(data)

# Main
def main() -> None:
    global verbose

    args = parse_args()
    verbose = args.verbose
    icon_size = args.icon

    if icon_size is None:
        render_icon = False
    else:
        render_icon = True
        icon_size = max(1, min(icon_size, 64))

    url = api_url(args.host, args.port)
    data = get_data(url)

    display_data(data, render_icon, icon_size)


if __name__ == "__main__":
    main()

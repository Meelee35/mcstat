from datetime import datetime

from mcstat.log import vprint, warn
from mcstat.motd_parser import format_motd


def display(data: dict) -> None:
    """Display api response neatly"""
    _display_motd(data.get("motd"))
    _display_version(data.get("version"))
    _display_players(data.get("players"))
    _display_mods(data.get("mods"))
    _display_plugins(data.get("plugins"))
    _verbose_server_info(data)

    if data.get("eula_blocked"):
        warn("This server has been blocked by Mojang for violating the EULA.")

def _verbose_server_info(data: dict):
    vprint("\n-- EXTRA INFO --")
    retrieved_at = data.get("retrieved_at")
    expires_at = data.get("expires_at")

    cache_date = datetime.fromtimestamp(retrieved_at / 1000) if retrieved_at else None
    cache_expiry = datetime.fromtimestamp(expires_at / 1000) if expires_at else None

    if cache_date:
        vprint(f"API cache created: {cache_date}")
    if cache_expiry:
        vprint(f"API cache expires: {cache_expiry}")

    hostname = data.get("host")
    ip = data.get("ip_address")
    if hostname:
        vprint(f"Resolved hostname: {hostname}")
    if ip:
        vprint(f"Resolved IP: {ip}")

    software = data.get("software")
    if software:
        vprint(f"Software: {software}")


def _display_mods(mods: list | None) -> None:
    if not mods:
        return
    print("Mods:")
    for i, mod in enumerate(mods):
        print(f"  {i}. {mod['name']} {mod['version']}")

def _display_plugins(plugins: list | None) -> None:
    if not plugins:
        return
    print("Plugins:")
    for i, plugin in enumerate(plugins, 1):
        print(f"  {i}. {plugin['name']} {plugin['version']}")

def _display_players(players_dict: dict | None) -> None:
    if not players_dict:
        warn("No player info provided.")
        return

    online = players_dict["online"]
    max_players = players_dict["max"]
    player_list = players_dict["list"]

    print(f"Players: {online} / {max_players}")

    if online > 0:
        if player_list:
            for i, player in enumerate(player_list, 1):
                print(f"{i}. {player['name_clean']}")
        else:
            print("No player list available")


def _display_version(version_dict: dict | None) -> None:
    if version_dict:
        print(f"Version: {version_dict['name_clean']}")
    else:
        warn("No version information provided")


def _display_motd(motd_dict: dict | None) -> None:
    if not motd_dict:
        warn("No MOTD available.")
        return
    
    print(format_motd(motd_dict["raw"]))
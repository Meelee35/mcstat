from mcstat.log import vprint, warn


def display(data: dict) -> None:
    _display_motd(data.get("motd"))
    _display_version(data.get("version"))
    _display_players(data.get("players"))


def _display_players(players_dict: dict | None) -> None:
    vprint(f"Players dict: {players_dict}")

    if not players_dict:
        warn("No player info provided.")
        return

    online = players_dict["online"]
    max_players = players_dict["max"]
    player_list = players_dict["list"]

    print(f"Players: {online} / {max_players}")

    if online > 0:
        print(", ".join(player["name_clean"] for player in player_list) if player_list else "No player list available")


def _display_version(version_dict: dict | None) -> None:
    vprint(version_dict)

    if version_dict:
        print(f"Version: {version_dict['name_clean']}")
    else:
        warn("No version information provided")


def _display_motd(motd_dict: dict | None) -> None:
    if not motd_dict:
        warn("No MOTD available.")
        return

    for line in motd_dict["clean"].splitlines():
        print(line.strip())
    print()
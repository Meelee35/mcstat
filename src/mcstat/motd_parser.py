import re

from mcstat.log import vprint

MOTD_COLORS = {
    "0": "\033[38;2;0;0;0m",         # black
    "1": "\033[38;2;0;0;170m",       # dark blue
    "2": "\033[38;2;0;170;0m",       # dark green
    "3": "\033[38;2;0;170;170m",     # dark aqua
    "4": "\033[38;2;170;0;0m",       # dark red
    "5": "\033[38;2;170;0;170m",     # dark purple
    "6": "\033[38;2;255;170;0m",     # gold
    "7": "\033[38;2;170;170;170m",   # gray
    "8": "\033[38;2;85;85;85m",      # dark gray
    "9": "\033[38;2;85;85;255m",     # blue
    "a": "\033[38;2;85;255;85m",     # green
    "b": "\033[38;2;85;255;255m",    # aqua
    "c": "\033[38;2;255;85;85m",     # red
    "d": "\033[38;2;255;85;255m",    # light purple
    "e": "\033[38;2;255;255;85m",    # yellow
    "f": "\033[38;2;255;255;255m",   # white
    "l": "\033[1m",                  # bold
    "o": "\033[3m",                  # italic
    "n": "\033[4m",                  # underline
    "m": "\033[9m",                  # strikethrough
    "r": "\033[0m",                  # reset
}

def _replace_code(code: str) -> str:
    return MOTD_COLORS.get(code, "\033[0m")

def format_motd(motd: str) -> str:
    """Convert raw motd formatting to ansi formatting"""
    vprint("Formatting motd: " + motd)

    temp = re.sub(" +", " ", motd)
    processed_motd = ""
    for line in temp.splitlines():
        processed_motd += re.sub(r'^(§.)\s+', r'\1', line) + "\n"

    result = ""

    i = 0
    while i < len(processed_motd):
        if processed_motd[i] == "§" and i + 1 < len(processed_motd):
            code = processed_motd[i+1]
            new_code = _replace_code(code)
            result += new_code
            i += 1
        else:
            result += processed_motd[i]

        i += 1
    vprint("Finished formatting: " + repr(result + "\033[0m"))
    return result + "\033[0m"

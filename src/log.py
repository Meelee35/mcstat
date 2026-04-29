import sys
from typing import NoReturn

verbose = False

def vhint() -> None:
    if not verbose:
        print("Use verbose mode for extra info. (-v)")


def vprint(*args, **kwargs) -> None:
    if verbose:
        print(*args, **kwargs)


def fatal(e: Exception | str, doing: str | None = None) -> NoReturn:
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

import sys
from typing import NoReturn

verbose = False

def vhint() -> None:
    if not verbose:
        print("Use verbose mode for extra info. (-v)")


def vprint(*args, **kwargs) -> None:
    if verbose:
        print(*args, **kwargs)

def _format_error(prefix: str, error: Exception | str, context: str | None) -> str:
    name = error if isinstance(error, str) else type(error).__name__
    msg = context or ""
    return f"{prefix}: {name} {msg}".strip()

def fatal(error: Exception | str, context: str | None = None) -> NoReturn:
    """Format and display a fatal error, then exit. Outputs full error details in verbose mode."""
    content = _format_error("Fatal", error, context)
    print(f"\033[31m{content}\033[0m")

    if isinstance(error, Exception):
        vhint()
        vprint(error)

    sys.exit(1)


def warn(error: Exception | str, context: str | None = None) -> None:
    """Format and display a warning. Outputs full error details in verbose mode."""
    content = _format_error("Warning", error, context)
    print(f"\033[33m{content}\033[0m")

    if isinstance(error, Exception):
        vhint()
        vprint(error)

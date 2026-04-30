import argparse

from mcstat.version import VERSION

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Server IP or hostname")
    parser.add_argument("port", nargs="?", type=int, default=25565, help="Server port (Default: 25565)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-i", "--icon", nargs="?", const=16, type=int, metavar="SIZE", help="Display server's icon instead of standard information (Default: 16px)")
    parser.add_argument("--version", action="version", version=f"mcstat {VERSION}", help="Print mcstat version")
    return parser.parse_args()
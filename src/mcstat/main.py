import requests

import mcstat.log as log
from mcstat.iconrenderer import IconRenderer
from mcstat.log import warn, fatal, vprint
from mcstat.arguments import parse_args
from mcstat.api_url import api_url
from mcstat.fetch_data import get_data
from mcstat.serverrenderer import display


# Main
def main() -> None:
    args = parse_args()
    
    log.verbose = args.verbose
    icon_size = args.icon

    if icon_size is None:
        render_icon = False
    else:
        render_icon = True
        icon_size = max(1, min(icon_size, 64))

    url = api_url(args.host, args.port)
    data = get_data(url)

    if render_icon:
        icon_renderer = IconRenderer(size=icon_size)
        icon_renderer.render(data)
    else:
        vprint("Displaying data")
        display(data)


if __name__ == "__main__":
    main()

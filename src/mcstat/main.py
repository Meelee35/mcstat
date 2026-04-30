import mcstat.log as log
from mcstat.iconrenderer import IconRenderer
from mcstat.log import warn, fatal, vprint
from mcstat.arguments import parse_args
from mcstat.api_url import api_url
from mcstat.fetch_data import get_data
from mcstat.serverrenderer import display


def main() -> None:
    args = parse_args()
    
    log.verbose = args.verbose
    icon_size = args.icon

    url = api_url(args.host, args.port)
    data = get_data(url)

    if icon_size is None:
        vprint("Displaying data")
        display(data)
    else:
        icon_size = max(1, min(icon_size, 64))
        icon_renderer = IconRenderer(size=icon_size)
        icon_renderer.render(data)


if __name__ == "__main__":
    main()

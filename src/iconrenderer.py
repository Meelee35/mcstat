from PIL import Image
import base64
import io

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

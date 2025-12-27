# filter.py
import io

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
from PIL import Image
from PIL import ImageFilter as PilFilter
from PIL import ImageOps


class ImageFilter(EventDispatcher):

    texture = ObjectProperty()

    def __init__(self, **kwargs) -> None:
        super(ImageFilter, self).__init__(**kwargs)
        # Register filters here
        self.filters = {
            "grayscale": self._grayscale,
            "sepia": self._sepia,
            "blur": self._blur,
            "reflection": self._reflect,
            "edges": self._edges,
        }

    def apply(self, filter_name, source):
        """
        Apply a filter to an image and return a Kivy Texture.
        :param filter_name: str, name of the filter
        :param source: str (path) or bytes buffer
        :return: kivy.graphics.texture.Texture
        """
        # Load image from path or buffer
        if isinstance(source, str):
            img = Image.open(source).convert("RGBA")
        elif isinstance(source, (bytes, bytearray, io.BytesIO)):
            img = Image.open(io.BytesIO(source)).convert("RGBA")
        else:
            raise ValueError("Unsupported source type")

        # Apply filter
        if filter_name not in self.filters:
            raise ValueError(f"Filter '{filter_name}' not supported")
        img = self.filters[filter_name](img)

        # Convert to Kivy Texture
        def _apply(dt):
            try:
                self.texture = self._to_texture(img)
            except Exception as e:
                print(e)

        Clock.schedule_once(_apply)
        return self._to_texture(img)

    # ---------------- FILTER IMPLEMENTATIONS ---------------- #

    def _grayscale(self, img):
        return ImageOps.grayscale(img).convert("RGBA")

    def _sepia(self, img):
        sepia_img = img.convert("RGBA")
        pixels = sepia_img.load()
        for y in range(sepia_img.height):
            for x in range(sepia_img.width):
                r, g, b, a = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255), a)

        return sepia_img

    def _blur(self, img: Image.Image) -> Image.Image:
        # Normalize and copy to avoid read-only / stream issues
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        work = img.copy()

        try:
            # Basic box blur equivalent to BLUR
            return work.filter(PilFilter.BLUR)
        except Exception:
            # Fallbacks that are widely supported
            try:
                return work.filter(PilFilter.BoxBlur(1))
            except Exception:
                return work.filter(PilFilter.GaussianBlur(1))

    def _reflect(self, img):
        return ImageOps.mirror(img)

    def _edges(self, img):
        # Normalize mode: FIND_EDGES works best on RGB
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        try:
            # Apply Pillow’s built-in edge detection
            edge_img = img.filter(PilFilter.FIND_EDGES)
        except Exception:
            # Fallback Laplacian kernel if FIND_EDGES fails
            kernel = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
            edge_img = img.filter(PilFilter.Kernel((3, 3), kernel, scale=1))

        # Convert back to RGBA for Kivy texture compatibility
        return edge_img.convert("RGBA")

    # ---------------- HELPER ---------------- #

    def _to_texture(self, img):
        """
        Convert Pillow Image to Kivy Texture.
        """
        img_data = img.tobytes()
        texture = Texture.create(size=img.size, colorfmt="rgba")
        texture.blit_buffer(img_data, colorfmt="rgba", bufferfmt="ubyte")
        texture.flip_vertical()
        return texture

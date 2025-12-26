# filter.py
# from PIL import Image, ImageOps, ImageFilter as PilFilter
from kivy.graphics.texture import Texture
import io

class ImageFilter:
    def __init__(self, **kwargs) -> None:
        super(ImageFilter, self).__init__(**kwargs)
        # Register filters here
        # self.filters = {
        #     "grayscale": self._grayscale,
        #     "sepia": self._sepia,
        #     "blur": self._blur,
        #     "reflection": self._reflect,
        #     "edges": self._edges
        # }

    # def apply(self, filter_name, source):
    #     """
    #     Apply a filter to an image and return a Kivy Texture.
    #     :param filter_name: str, name of the filter
    #     :param source: str (path) or bytes buffer
    #     :return: kivy.graphics.texture.Texture
    #     """
    #     # Load image from path or buffer
    #     if isinstance(source, str):
    #         img = Image.open(source).convert("RGBA")
    #     elif isinstance(source, (bytes, bytearray, io.BytesIO)):
    #         img = Image.open(io.BytesIO(source)).convert("RGBA")
    #     else:
    #         raise ValueError("Unsupported source type")

    #     # Apply filter
    #     if filter_name not in self.filters:
    #         raise ValueError(f"Filter '{filter_name}' not supported")
    #     img = self.filters[filter_name](img)

    #     # Convert to Kivy Texture
    #     return self._to_texture(img)

    # # ---------------- FILTER IMPLEMENTATIONS ---------------- #

    # def _grayscale(self, img):
    #     return ImageOps.grayscale(img).convert("RGBA")

    # def _sepia(self, img):
    #     sepia_img = img.convert("RGBA")
    #     pixels = sepia_img.load()
    #     for y in range(sepia_img.height):
    #         for x in range(sepia_img.width):
    #             r, g, b, a = pixels[x, y]
    #             tr = int(0.393 * r + 0.769 * g + 0.189 * b)
    #             tg = int(0.349 * r + 0.686 * g + 0.168 * b)
    #             tb = int(0.272 * r + 0.534 * g + 0.131 * b)
    #             pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255), a)

    #     return sepia_img

    # def _blur(self, img):
    #     return img.filter(PilFilter.BLUR)

    # def _reflect(self, img):
    #     return ImageOps.mirror(img)

    # def _edges(self, img):
    #     # Edge detection using Pillow’s built-in filter
    #     return img.filter(PilFilter.FIND_EDGES)

    # # ---------------- HELPER ---------------- #

    # def _to_texture(self, img):
    #     """
    #     Convert Pillow Image to Kivy Texture.
    #     """
    #     img_data = img.tobytes()
    #     texture = Texture.create(size=img.size, colorfmt='rgba')
    #     texture.blit_buffer(img_data, colorfmt='rgba', bufferfmt='ubyte')
    #     texture.flip_vertical()
    #     return texture
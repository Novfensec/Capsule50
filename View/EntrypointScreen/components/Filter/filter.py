from View.base_screen import BaseScreenView


class Filter(BaseScreenView):

    def __init__(self, **kwargs) -> None:
        super(Filter, self).__init__(**kwargs)
        self.cs50x_desc = """The CS50 Filter problem challenges students to manipulate digital images at the pixel level using C. Each image is represented as a grid of pixels, with every pixel defined by three values—red, green, and blue (RGB). The task is to implement functions that apply transformations such as converting an image to grayscale, giving it a sepia tone, reflecting it horizontally, or blurring it by averaging neighboring pixels. By working through these filters, students gain hands-on experience with arrays, loops, and structs, while also learning how mathematical operations can alter visual data. This problem bridges theory and practice, showing how low-level programming concepts directly affect how images are processed and displayed.
        """

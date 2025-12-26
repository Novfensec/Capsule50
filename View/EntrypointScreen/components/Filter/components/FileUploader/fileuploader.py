from carbonkivy.uix.boxlayout import CBoxLayout
from libs.fileuploader import CFileUploader
from kivy.properties import StringProperty
# from plyer import filechooser


class FileUploader(CFileUploader, CBoxLayout):
    description = StringProperty()

    data_source = StringProperty(None, allownone=True)

    def __init__(self, **kwargs) -> None:
        super(FileUploader, self).__init__(**kwargs)
        self.filters = {
            "All Images": ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"],
            "JPEG Files": ["*.jpg", "*.jpeg"],
            "PNG Files": ["*.png"],
        }

    def on_file(self, *args) -> None:
        if self.file:
            self.description = self.file
        else:
            self.description = "Upload an image"

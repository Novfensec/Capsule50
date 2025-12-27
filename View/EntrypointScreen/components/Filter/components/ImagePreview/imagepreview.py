import threading

from carbonkivy.uix.anchorlayout import CAnchorLayout
from carbonkivy.uix.dropdown import CDropdown
from carbonkivy.uix.modal import CModal
from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, StringProperty

from libs.filter import ImageFilter


class TypeFilterDropdown(CDropdown):

    def __init__(self, **kwargs) -> None:
        super(TypeFilterDropdown, self).__init__(**kwargs)


class Preview(EventDispatcher):

    source = StringProperty(None, allownone=True)

    dropdown = ObjectProperty()

    def __init__(self, **kwargs) -> None:
        super(Preview, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.ft = ImageFilter()
        self.ft.bind(texture=self.on_texture)

    def on_kv_post(self, base_widget) -> None:
        self.dropdown = TypeFilterDropdown(
            master=self.ids.filter_btn, pos=self.ids.filter_btn.pos
        )
        return super().on_kv_post(base_widget)

    def apply_filter(self, *args) -> None:
        self.app.loading_state(True, master=self)
        type_filter = ""
        for item in self.dropdown.ids.selection_layout.children:
            if hasattr(item, "selected") and item.selected:
                type_filter = item.name.lower()
        thread = threading.Thread(
            target=self.ft.apply,
            kwargs={"filter_name": type_filter, "source": self.source},
        )
        thread.start()

    def on_texture(self, instance: object, texture: object, *args) -> None:
        self.ids.img_source.texture = texture
        self.ids.img_source.canvas.ask_update()
        self.app.loading_state(False, master=self)


class WindowPreview(Preview, CModal):

    source = StringProperty(None, allownone=True)

    def __init__(self, **kwargs) -> None:
        super(WindowPreview, self).__init__(**kwargs)

    def dismiss(self):
        try:
            Window.remove_widget(self)
        except Exception as e:
            return


class ImagePreview(Preview, CAnchorLayout):

    def __init__(self, **kwargs) -> None:
        super(ImagePreview, self).__init__(**kwargs)
        self.window_preview = WindowPreview()

    def preview(self, *args):
        self.window_preview.source = self.source
        try:
            Window.add_widget(self.window_preview)
        except Exception as e:
            return

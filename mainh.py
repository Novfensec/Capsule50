import os
import sys

os.environ["devicetype"] = "mobile"

from View.base_screen import LoadingLayout
from kivy.uix.screenmanager import FadeTransition as FT
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.devtools import LiveApp
from carbonkivy.app import CarbonApp
import webbrowser
from kivy.properties import ColorProperty
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
import importlib

from kivy.resources import resource_add_path

import registers

sys.path.insert(0, os.path.dirname(__file__))
resource_add_path(os.path.dirname(__file__))


from kivy import Config
from PIL import ImageGrab

resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "1280")
Config.set("graphics", "width", "317")

from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width + 5


class UI(CScreenManager):

    def __init__(self, *args, **kwargs) -> None:
        super(UI, self).__init__(*args, **kwargs)
        self.transition = FT(duration=0.05, clearcolor=[1, 1, 1, 0])


class Capsule50(CarbonApp, LiveApp):

    def __init__(self, *args, **kwargs) -> None:
        self.theme = "Gray100"
        super(Capsule50, self).__init__(*args, **kwargs)
        self.loading_layout = LoadingLayout()

    def build_app(self) -> UI:
        self.manager_screens = UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Adds different screen widgets to the screen manager
        """
        import View.screens

        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            view = screens[name_screen]["object"](view_model=model)
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)

    @mainthread
    def ban_state(self, state: bool = False, master: object = Window, *args) -> None:
        try:
            if state:
                master.add_widget(self.ban_layout)
            else:
                master.remove_widget(self.ban_layout)
        except:
            return None

    @mainthread
    def loading_state(
        self, state: bool = False, master: object = Window, *args
    ) -> None:
        try:
            if state:
                master.add_widget(self.loading_layout)
            else:
                master.remove_widget(self.loading_layout)
        except:
            return None


if __name__ == "__main__":
    Capsule50().run()

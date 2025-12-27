"""
The entry point to the application.

The application uses the MVVM template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.
"""

# ==========================
# Standard Library Imports
# ==========================
import os
import sys

from kivy.resources import resource_add_path

os.environ["devicetype"] = "mobile"

sys.path.insert(0, os.path.dirname(__file__))
resource_add_path(os.path.dirname(__file__))

import ssl
import webbrowser

from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager

# ==========================
# Third-Party Library Imports
# ==========================
from kivy.clock import Clock, mainthread
from kivy.core.window import Window

import registers

# ==========================
# Custom Module Imports
# ==========================
from View.base_screen import LoadingLayout

# ==========================
# SSL Configuration
# ==========================
ssl._create_default_https_context = ssl._create_unverified_context


Clock.max_iteration = 60


def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))


class UI(CScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)


class Capsule50(CarbonApp):

    def __init__(self, **kwargs):
        self.theme = "White"
        super(Capsule50, self).__init__(**kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))
        self.loading_layout = LoadingLayout()

    def build(self) -> UI:
        # This is the screen manager that will contain all the screens of your application.
        self.manager_screens = UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        # adds different screen widgets to the screen manager
        import View.screens

        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            view = screens[name_screen]["object"](view_model=model)
            model.add_observer(view)
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
    app = Capsule50()
    app.run()

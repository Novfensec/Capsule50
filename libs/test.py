import json
import os
import random

from carbonkivy.app import CarbonApp
from carbonkivy.uix.boxlayout import CBoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class Bar(Widget):
    def __init__(self, value, **kwargs):
        super(Bar, self).__init__(**kwargs)
        self.height = value
        with self.canvas:
            # default blue
            self.color = Color(*CarbonApp.get_running_app().interactive[:3], 1)
            self.rect = Rectangle(pos=self.pos, size=(self.width, self.height))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.width, self.height)

    def set_color(self, crgba):
        """Accepts a Carbon color token (RGBA list/tuple) and applies it."""
        r, g, b, a = crgba
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a


class SortVisualizer(CBoxLayout):

    name_sort = StringProperty("insertion")  # default to insertion sort

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = CarbonApp.get_running_app()
        self.bars = []
        content = ""
        with open(
            os.path.join(os.path.dirname(__file__), "env.json"), "r", encoding="utf-8"
        ) as env_file:
            content = json.load(env_file)
        self.name_sort = content["namesort"]
        self.app.name_sort = self.name_sort
        self.data = [random.randint(64, 300) for _ in range(15)]

        for val in self.data:
            bar = Bar(dp(val))
            self.add_widget(bar)
            self.bars.append(bar)

        self.sorting_steps = {
            "bubble": self.bubble_sort_steps,
            "selection": self.selection_sort_steps,
            "insertion": self.insertion_sort_steps,
        }
        self.steps = list(self.sorting_steps[self.name_sort](self.data[:]))
        Clock.schedule_interval(self.next_step, 0.5)

    def bubble_sort_steps(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                yield ("compare", j, j + 1)
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    yield ("swap", j, j + 1)

    def selection_sort_steps(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                yield ("compare", min_idx, j)
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield ("swap", i, min_idx)

    def insertion_sort_steps(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            # Highlight the key bar
            yield ("key", i, None)
            while j >= 0 and arr[j] > key:
                yield ("compare", j, j + 1)
                arr[j + 1] = arr[j]
                yield ("swap", j, j + 1)
                j -= 1
            arr[j + 1] = key
            yield ("insert", j + 1, i)

    def next_step(self, dt):
        if not self.steps:
            return False
        action, i, j = self.steps.pop(0)

        # Reset all bars to blue
        for bar in self.bars:
            bar.set_color(self.app.blue_50)

        if action == "compare":
            self.bars[i].set_color(self.app.red_70)
            self.bars[j].set_color(self.app.red_70)

        elif action == "swap":
            bar1, bar2 = self.bars[i], self.bars[j]
            anim1 = Animation(x=bar2.x, duration=0.2)
            anim2 = Animation(x=bar1.x, duration=0.2)
            anim1.start(bar1)
            anim2.start(bar2)
            self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
            self.bars[i].set_color(self.app.red_50)
            self.bars[j].set_color(self.app.red_50)

        elif action == "key":
            self.bars[i].set_color(self.app.yellow_50)

        elif action == "insert":
            self.bars[i].set_color(self.app.green_60)


class SortApp(CarbonApp):

    name_sort = StringProperty("insertion")

    def build(self):
        self.app_kv = """
CScreen:
    CLabel:
        text: st.name_sort.capitalize() + f' Sort'
        style: "heading_05"
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y": 0.8}

    SortVisualizer:
        id: st
        orientation: "horizontal"
        spacing: dp(4)
        size_hint: 1, 1
        padding: [0, 0, 0, dp(64)]

<Bar>:
    size_hint: None, None
    width: dp(16)
        """
        return Builder.load_string(self.app_kv)


if __name__ == "__main__":

    SortApp().run()

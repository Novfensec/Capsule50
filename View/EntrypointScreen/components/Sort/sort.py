import os, sys
import subprocess # nosec

from View.base_screen import BaseScreenView
from kivy.utils import platform
if platform == "android":
    from libs.launcher.android import launch_client_activity


class Sort(BaseScreenView):

    def __init__(self, **kwargs) -> None:
        super(Sort, self).__init__(**kwargs)

    def run_entrypoint(self, namesort: str | None = None) -> None:
        entrypoint_path = os.path.abspath(
            os.path.join(os.getcwd(), "libs", "test.py")
        )
        target_dir = os.path.dirname(entrypoint_path)
        try:
            if platform == "android":
                launch_client_activity(entrypoint_path)
            else:
                os.environ["namesort"] = namesort
                self.process = subprocess.Popen(
                    [sys.executable, entrypoint_path], cwd=target_dir, env=os.environ
                )  # nosec
                print(f"[RUN] {os.path.basename(entrypoint_path)} launched...")
        except Exception as e:
            print(e)
            self.notify(
                status="Error",
                title="Error",
                subtitle=f"{e}",
                variant="Toast",
            )
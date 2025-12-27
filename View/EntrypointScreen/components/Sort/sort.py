import json
import os
import subprocess  # nosec
import sys

from kivy.utils import platform

from View.base_screen import BaseScreenView

if platform == "android":
    from libs.launcher.android import launch_client_activity


class Sort(BaseScreenView):

    def __init__(self, **kwargs) -> None:
        super(Sort, self).__init__(**kwargs)

    def run_entrypoint(self, namesort: str | None = None) -> None:
        entrypoint_path = os.path.abspath(
            os.path.join(self.app.directory, "libs", "test.py")
        )
        target_dir = os.path.dirname(entrypoint_path)
        try:
            if platform == "android":
                launch_client_activity(entrypoint_path)
            else:
                with open(
                    os.path.join(target_dir, "env.json"), "w", encoding="utf-8"
                ) as env_file:
                    json.dump(
                        {"namesort": namesort}, env_file, ensure_ascii=False, indent=4
                    )

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

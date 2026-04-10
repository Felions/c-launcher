from pathlib import Path
import readline
import os

def input_with_default(prompt, default):
    readline.set_startup_hook(lambda: readline.insert_text(default))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def init():
    path = Path.home() / ".c-launcher/saved/settings.json"
    if not os.path.exists(path):
        os.mkdir(Path.home() / ".c-launcher")
        os.mkdir(Path.home() / ".c-launcher/saved")
        os.mkdir(Path.home() / ".c-launcher/pfx")
        with open(path, "w") as f:
            f.write("{}")

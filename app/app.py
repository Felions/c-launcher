from pathlib import Path
import subprocess
import json
import sys
import os

class App:
    def __init__(self, game=""):
        # 1. Read saved settings
        with open(Path.home() / ".c-launcher/saved/settings.json", "r") as f:
            self.data = json.loads(f.read())

        if game != "":
            self.start(game)
            sys.exit()

        self.actions = {"help": ["Show this message", self.help],
                        "list": ["List games", self.show],
                        "quit": ["Quits shell", sys.exit],
                        "run": ["Runs game, useage: run [game]", self.start]}
    
    def save(self):
        with open(Path.home() / ".c-launcher/saved/settings.json", "w") as f:
            f.write(json.dumps(self.data, default=str))
    
    def add(self,
            display_name: str,
            executable_path: str,
            platform: str= None,
            prefix_path: str= None,
            proton_path: str= None,
            aliases: list[str]= None):
        
        if platform is None:
            if executable_path.split(".")[-1] == "exe":
                platform = "windows"
            else:
                platform = "linux"

        if prefix_path is None:
            if platform != "linux":
                prefix_path = Path.home() / ".c-launcher/pfx/{}".format(display_name)

        if proton_path is None:
            proton_path = ""

        if aliases is None:
            aliases = []
        else:
            all = []
            for value in self.data.values():
                all.extend(value["aliases"])
            for alias in aliases:
                if alias in all:
                    print("Alias '{}' already in use".format(alias))
                    return


        self.data[display_name] = {
            "executable_path": executable_path,
            "platform": platform,
            "prefix_path": prefix_path,
            "proton_path": proton_path,
            "aliases": aliases
        }

        self.save()

    def show(self):
        for key, value in self.data.items():
            print("~ {} - {}".format(key, ", ".join(i for i in value["aliases"])))
    
    def start(self, game: str, in_place: bool):

        if game not in self.data.keys():
            for key, value in self.data.items():
                for i in value["aliases"]:
                    if i == game:
                        game = key

        command = []
        env = os.environ.copy()
        if self.data[game]["platform"] == "windows":
            if self.data[game]["proton_path"] != "":
                env["PROTONPATH"] = self.data[game]["proton_path"]
            env["WINEPREFIX"] = self.data[game]["prefix_path"]
            command.append("umu-run")
            command.append("{}".format(self.data[game]["executable_path"]))
        else:
            command.append("{}".format(self.data[game]["executable_path"]))
        
        if in_place == False:
            subprocess.Popen(command, 
                               env=env, 
                               start_new_session=True, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, env=env)

    def help(self):
        for i, j in self.actions.items():
            print(f"{i}: {j[0]}")

    def run(self):
        while True:
            action = input("$> ").split(" ")
            self.actions[action[0]][1](*action[1:])
            

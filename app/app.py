from pathlib import Path
from app.utils import *
import subprocess
import json
import sys
import os

class App:
    def __init__(self, game=""):
        init()
        # 1. Read saved settings
        with open(Path.home() / ".c-launcher/saved/settings.json", "r") as f:
            self.data = json.loads(f.read())

        if game != "":
            self.start(game)
            sys.exit()

        self.actions = {"help": ["Show this messeage", self.help],
                        "list": ["List games", self.show],
                        "quit": ["Quits shell", sys.exit],
                        "run": ["Runs game, useage: run [game]\n\t Add -i for running in place", self.start],
                        "info": ["Prints [game] information", self.info],
                        "edit": ["Edits game info, useage: edit [game]", self.edit],
                        "remove": ["Removes game from launcher, useage: edit [game]", self.remove]}
    
    def remove(self, args):
        if type(args) != str:
            game = " ".join(i for i in args)
        else:
            game = args
        if game not in self.data.keys():
            for key, value in self.data.items():
                for i in value["aliases"]:
                    if i == game:
                        game = key
        if game not in self.data.keys():
            print("Can't find '{}'".format(game))
            return
        
        self.data.pop(game, None)
        self.save()
        print("{} was removed".format(game))

    def info(self, args):
        if type(args) != str:
            game = " ".join(i for i in args)
        else:
            game = args
        if game not in self.data.keys():
            for key, value in self.data.items():
                for i in value["aliases"]:
                    if i == game:
                        game = key
        if game not in self.data.keys():
            print("Can't find '{}'".format(game))
            return
        
        print("""
Executable path: {}
Platform: {}
Prefix path: {}
Proton path: {}
Aliases: {}
        """.format(
              self.data[game]["executable_path"],
              self.data[game]["platform"],
              self.data[game]["prefix_path"],
              self.data[game]["proton_path"],
              ", ".join(i for i in self.data[game]["aliases"])
              ))


    def edit(self, args: list[str]):

        game = " ".join(i for i in args)

        if game not in self.data.keys():
            for key, value in self.data.items():
                for i in value["aliases"]:
                    if i == game:
                        game = key
        if game not in self.data.keys():
            print("Can't find '{}'".format(game))
            return
        
        print("""
Pass -m flag to modify, E.g. e -m

Executable path [e]: {}
Platform [pl]: {}
Prefix path [pf]: {}
Proton path [pr]: {}
Aliases [a]: {} - Please seperate aliases with comma 
        """.format(
              self.data[game]["executable_path"],
              self.data[game]["platform"],
              self.data[game]["prefix_path"],
              self.data[game]["proton_path"],
              ", ".join(i for i in self.data[game]["aliases"])
              ))

        mod = input("What to modify: ").split(" ")

        modify = False
        if "-m" in mod:
            modify = True

        match mod[0]:
            case "e":
                what = "executable_path"
            case "pl":
                what = "platform"
            case "pf":
                what = "prefix_path"
            case "pr":
                what = "proton_path"
            case "a":
                what = "aliases"
            case _:
                print("Wrong option")
                return

        if modify:
            if what != "aliases":
                old_data = self.data[game][what]
            else:
                old_data = ", ".join(self.data[game][what])
            
            new_data = input_with_default("", "{}".format(old_data))
        else:
            new_data = input("{} >".format(what))
        
        if what != "aliases":
            self.data[game][what] = new_data
        else:
            new_data = new_data.replace(" ", "").split(",")
            all = []
            for key, value in self.data.items():
                if key == game:
                    continue
                all.extend(value["aliases"])
            for alias in new_data:
                if alias in all:
                    print("Alias '{}' already in use".format(alias))
                    return
 
            self.data[game][what] = new_data

        self.save()
     
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

    def show(self, args):
        for key, value in self.data.items():
            print("~ {} - {}".format(key, ", ".join(i for i in value["aliases"])))
    
    def start(self, args, in_place=False): #game: str, in_place=False):
        
        if "-i" in args:
            in_place = True
            args.remove("-i")

        game = " ".join(i for i in args)

        if game not in self.data.keys():
            for key, value in self.data.items():
                for i in value["aliases"]:
                    if i == game:
                        game = key
        
        if game not in self.data.keys():
            print("Can't find '{}'".format(game))
            return

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

    def help(self, args):
        print()
        for i, j in self.actions.items():
            print(f"{i}: {j[0]}")
        print()

    def run(self):
        try:
            while True:
                action = input("$> ").split(" ")
                try:
                    self.actions[action[0]][1](action[1:])
                except KeyError:
                    print("Try asking for 'help' ;)")
        except EOFError, KeyboardInterrupt:
            sys.exit()

 

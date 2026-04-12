#!/usr/bin/python

from app import App
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog= "c-launcher",
        description= "Simple cli launcher for games"
    )
    parser.add_argument("game", nargs='?', default=None, help="Runs [game]")
    parser.add_argument("-i", "--in_place", action="store_true", default=False, help="Runs [game] in this terminal window")
    parser.add_argument("-l", "--list", action="store_true", default=False, help="Lists games and exits")
    parser.add_argument("-v", "--version", action="store_true", default=False, help="Prints version and exits")
    parser.add_argument("--info", action="store_true", default=False, help="Prints [game] information and exits")
    parser.add_argument("-a", "--add", help="Adds [game] to launcher")
    parser.add_argument("-e", "--executable_path", help="Path to executable")
    parser.add_argument("-p", "--platform", default=None, help="Platform for which the game was created [windows/linux]")
    parser.add_argument("--proton_path", default=None, help="Path to proton, if left empty UmU-Proton will be used")
    parser.add_argument("--prefix_path", default=None, help="Path to wine prefix, if left empty new prefix will be created in ~/.c-launcher/pfx/[game]")
    parser.add_argument("--aliases", nargs="+", default=None, help="aliases that can be used to start the [game]")
    args = parser.parse_args()

    app = App()
    
    if args.version:
        print("v0.4.2")
        sys.exit()

    if args.info:
        app.info(args.game)
        sys.exit()

    if args.list:
        app.show(None)
        sys.exit()

    if args.game is not None:
        app.start(args.game, args.in_place)
        sys.exit()
    
    if args.add is not None and args.executable_path is not None:
        app.add(args.add,
                args.executable_path,
                platform=args.platform,
                prefix_path=args.prefix_path,
                proton_path=args.proton_path,
                aliases=args.aliases)
        sys.exit()

    if args.add is not None or args.executable_path is not None:
        if args.executable_path is None:
            print("No path to executable provided")
            sys.exit()
        if args.add is None:
            print("No name for the game provided")
            sys.exit()

    app.run()


if __name__ == "__main__":
    main()

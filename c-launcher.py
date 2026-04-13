#!/usr/bin/python

from app import App
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog= "c-launcher",
        description= "Simple cli launcher for games"
    )
    
    subparsers = parser.add_subparsers(dest="command")

    parser_a = subparsers.add_parser("run", help="Run [game]")
    parser_a.add_argument("game", default=None, help="Game title or alias")
    parser_a.add_argument("-i", "--in_place", action="store_true", default=False, help="Runs [game] in this terminal window")
   
    parser_b = subparsers.add_parser("add", help="Adds [game] to launcher")
    parser_b.add_argument("-n", "--name", default=None, help="The main name of the game")
    parser_b.add_argument("-e", "--executable_path", default=None, help="Path to executable")
    parser_b.add_argument("-p", "--platform", default=None, help="Platform for which the game was created [windows/linux]")
    parser_b.add_argument("--proton_path", default=None, help="Path to proton, if left empty UmU-Proton will be used")
    parser_b.add_argument("--prefix_path", default=None, help="Path to wine prefix, if left empty new prefix will be created in ~/.c-launcher/pfx/[game]")
    parser_b.add_argument("--aliases", nargs="+", default=None, help="aliases that can be used to start the [game]")

    parser_c = subparsers.add_parser("info", help="Prints [game] information")
    parser_c.add_argument("game", default=None, help="Game title or alias")
    
    parser_d = subparsers.add_parser("list", help="Lists games")
    
    parser_e = subparsers.add_parser("remove", help="Removes [game] from launcher")
    parser_e.add_argument("game", default=None, help="Game title or alias")
    
    parser.add_argument("-v", "--version", action="store_true", default=False, help="Prints version and exits")
    
    args = parser.parse_args()

    app = App()
    
    match args.command:
        case "run":
            if args.game is not None:
                app.start(args.game, in_place=args.in_place)
                sys.exit()

        case "add":
            if args.name is not None and args.executable_path is not None:
                app.add(args.name,
                    args.executable_path,
                    platform=args.platform,
                    prefix_path=args.prefix_path,
                    proton_path=args.proton_path,
                    aliases=args.aliases)
            else:
                print("Name and executable_path are required to add the game to launcher")
            sys.exit()
        
        case "info":
            if args.game is not None:
                app.info(args.game)
                sys.exit()
        
        case "remove":
            if args.game is not None:
                app.remove(args.game)
                sys.exit()
        
        case "list":
            app.show()
            sys.exit()

    if args.version:
        print("v0.4.3")
        sys.exit()

    app.run()


if __name__ == "__main__":
    main()

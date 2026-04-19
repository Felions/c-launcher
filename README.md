# c-launcher
## Description
### What is this?
It's simple cli for launching windows and native linux games, with prefix and proton management utility.
### How it works?
It uses [umu-launcher](https://github.com/Open-Wine-Components/umu-launcher) for windows games, and simple python code for prefix and proton management
### Why c-launcher?
coz i like letter c
## Usage
```
usage: c-launcher [-h] [-v] {run,add,info,list,remove} ...

Simple cli launcher for games

positional arguments:
  {run,add,info,list,remove}
    run                 Run [game]
    add                 Adds [game] to launcher
    info                Prints [game] information
    list                Lists games
    remove              Removes [game] from launcher

options:
  -h, --help            show this help message and exit
  -v, --version         Prints version and exits
```
btw u can get more info on positional arguments by adding -h to them ;)
## Installation
I provided an appimage in releases page, u just need to download it,  place it in ~/.local/bin and make it executable or just run: 
```
wget https://github.com/Felions/c-launcher/releases/latest/download/c-launcher.AppImage -O ~/.local/bin/c-launcher.AppImage && chmod u+x ~/.local/bin/c-launcher.AppImage
```

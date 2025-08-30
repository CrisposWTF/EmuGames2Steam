EmuGames2Steam
==============

I made this script to add emulator games as 'Non-Steam games', just because I don't like to play ps1 and ps2 games from retroarch.

I made this to add games that I use with the emulators 'PCSX2' and 'Duckstation'. I haven't test it with other emulators and only tested on my Linux machine (Pop_OS! 22.04), but you can use it as base and modify it as you like to add other things and test on other OS.

I know that there may be an app that do the same, but I was bored after work and with free time haha.

To use this, you need to set the necessary paths and file names for the script to run correctly

| Variable | Description |
----------|-------------
| emu_path | The path where your emulator is stored (ex: `/home/user/emulator` or `C:\\Program Files\\Emulator`)|
| emu_exec | The name of the emulator executable (ex: `pcsx2-v2.5.105-linux-appimage-x64-Qt.AppImage`) |
| emulator_commands | Commands specific to the emulator to use, for PCSX2 you can check the available commands [here](https://wiki.pcsx2.net/Command-line_support#General_Options_QT), and for DuckStation [here.](https://github.com/stenzek/duckstation/wiki/Command-Line-Arguments) |
| steam_userdata_folder_path | Your steam userdata folder (e.g., For Linux `/home/user/.steam/steam/userdata` and for Windows `C:\\Program Files (x86)\\Steam\\userdata`) where your user folder with the config folder that contains the shortcuts file is located. |

After setting this variables, you are good to go.

Disclaimer
==========

The content of this script is provided on an 'as is' basis, without warranty of any kind, express or implied, regarding its completeness, accuracy, or fitness for a particular purpose. The creator assumes no responsibility for any errors or omissions in the content.
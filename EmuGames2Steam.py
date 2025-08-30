import vdf
import psutil
import os, re, json, signal, time, shutil
from pathlib import Path

def check_steam_running():
    """Finds the PID of the Steam process."""
    for proc in psutil.process_iter(['pid', 'name']):
        if 'steam' in proc.info['name'].lower():
            return proc.info['pid']
    return None

def kill_process_by_pid(pid):
    """Kills a process given its PID."""
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(5)
        print(f"Process with PID {pid} terminated.")
    except ProcessLookupError:
        raise Exception(f"There's no process running with the PID {pid}.")
    except Exception as e:
        raise Exception(f"An error has occurred while trying to kill a process with the PID {pid}: {e}")

def add_to_steam(name: str, exe_path: str, steam_path, start_dir="", launch_options=""):
    #A backup of the vdf file will be created in this route
    backup_path = Path.home() / "Documents/shortcuts.vdf.bkp"
    user_dirs = [d for d in steam_path.iterdir() if d.is_dir() and d.name.isdigit()]
    
    if not user_dirs:
        print("No Steam user found")
        return;
    
    shortcut_file = user_dirs[0] / "config/shortcuts.vdf"
    #now we read the file
    shortcut_data = {'shortcuts': {}}
    if shortcut_file.exists():
        #If the file exists a backup is created
        shutil.copy2(shortcut_file, backup_path)
        with open(shortcut_file, 'rb') as f:
            shortcut_data = vdf.binary_load(f)
            #now we add the game to the shortcuts array
            newId = len(shortcut_data['shortcuts'])
            
            shortcut_data['shortcuts'][str(newId)] = {
                'AppName': name,
                'Exe': exe_path,
                'StartDir': start_dir,
                'icon': '',
                'ShortcutPath': '',
                'LaunchOptions': launch_options,
                'IsHidden': 0,
                'AllowDesktopConfig': 1,
                'AllowOverlay': 1,
                'OpenVR': 0,
                'Devkit': 0,
                'DevkitGameID': '',
                'DevkitOverrideAppID': 0,
                'LastPlayTime': 0,
                'FlatpakAppID': '',
                'tags': {}
            }
            with open(shortcut_file, 'wb') as f:
                vdf.binary_dump(shortcut_data, f)
                
            print(f'Added {name} to Steam')


def game_shortcuts(emulator_path: str, emu_exe: str, games_path: str, steam_path:str , emulator_commands:str=""):
    gamesFolder = os.scandir(games_path)
    for game in gamesFolder:
        if game.is_file():
            full_game_name = game.name
            game_name, game_ext = os.path.splitext(full_game_name)
            #regex the name (ex: Ape Escape 2 (USA).iso --> Ape\ Escape\ 2\ \(USA\).iso)
            escaped_full_name = re.sub(r'([ ()])', r'\\\1', full_game_name)
            full_game_path = os.path.join(games_path,escaped_full_name)
            exe_path = f'{emulator_path}/{emu_exe}  {full_game_path}  {emulator_commands}'
            add_to_steam(game_name,exe_path,steam_path,emulator_path)
            
    
def check_steam_shortcut_file(steam_path):
    json_doc = Path.home() / "Documents/steamShortcutData.json"
    userDirs = [d for d in steam_path.iterdir() if d.is_dir() and d.name.isdigit()]
    
    if not userDirs:
        print("No Steam user found")
        return;
    
    shortcut_file = userDirs[0] / "config/shortcuts.vdf"
    
    shortcut_data = {'shortcuts': {}}
    if shortcut_file.exists():
        with open(shortcut_file, 'rb') as f:
            shortcut_data = vdf.binary_load(f)
            with open(json_doc, 'w') as json_data:
                json_data.write(json.dumps(shortcut_data))
    print(f'Shortcuts data saved to {json_doc}')

def main():
    try:
        emu_path = '/path/to/Emulator'
        emu_exec = 'emulator.exe' # or emulator.AppImage
        emulator_commands = '' # emulator specific commands like (PCSX2) '-nogui -batch -slowboot'
        games_path = '/path/to/games'
        steam_userdata_folder_path = '/path/to/steam/userdata/folder' # e.g., Path.home() / ".steam/steam/userdata" or C:\\Program Files (x86)\\Steam\\userdata
        #the process of adding game shortcuts to steam, requires to have steam closed, just to not f up the shortcuts file
        #even with closing steam, I make a backup of the file just in case.
        steam_pid = check_steam_running()
        if steam_pid is not None:
            print("Closing steam...")
            kill_process_by_pid(steam_pid)
            print("Let's continue!")
        game_shortcuts(emu_path,emu_exec,games_path, steam_userdata_folder_path,emulator_commands)
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    main()
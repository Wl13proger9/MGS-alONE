import sys
import subprocess

from configparser import ConfigParser
from .req import DATA_PATH

import os
import locale



def on_error() -> None:
    pass


def localisation(section:str, key:str, forced_en:bool = False) -> str:
    locale.setlocale(locale.LC_ALL, "")
    lang = locale.getlocale()

    #print(lang)  

    try:
        config = ConfigParser()
        if forced_en:
            config.read(os.path.join(DATA_PATH, "local_en.ini"), encoding="utf-8")

        else:
            if "Russian_Russia" in lang:
                config.read(
                            os.path.join(DATA_PATH, "local_ru.ini"), 
                            encoding="utf-8"
                        )
            else:
                config.read(
                            os.path.join(DATA_PATH, "local_en.ini"), 
                            encoding="utf-8"
                        )

        return config.get(section, key, fallback = "...")
    except:return '...'


def clear_screen() -> None:
    cmd = "cls" if sys.platform == "win32" else "clear"
    subprocess.run(cmd, shell=True)


def get_config(file:str, section: str, key:str, value_type:str = 'str') -> str:   
    try:
        config = ConfigParser()

        config.read(
                    os.path.join(DATA_PATH, file), 
                    encoding="utf-8"
                )

        match value_type:
            case "str": 
                out = config.get(section, key, fallback = "...")

            case "int": 
                out = config.getint(section, key, fallback = "...")

            case "bool": 
                out = config.getboolean(section, key, fallback = "...")


            case _: 
                out = config.get(section, key, fallback = "...")

               
        return out 
    except: return '...'

    
def set_config() -> None:
    2


if __name__ == "__main__":
    print( localisation('Test', 'test'      ) )
    print( localisation('Test', 'test', True) )
    print( localisation('Test', 'testaaaaa' ) )

    print('----------------------------------')

    print( get_config('config.ini', 'General', 'animations', 'bool') )    
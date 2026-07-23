from .req import *
from .tui import *
from .hq  import *


clear_screen()


def start_game() -> None:
    clear_screen()
    input("Запуск")


def params() -> None:
    print("Настройки")


def cli_exit() -> None:
    sys.exit()


def on_nothing() -> None:
    print('Выбранный вами пункт не может быть выполнен..')


def main() -> None:
    colored_logo = LOGO.replace("█",hex_to_rgb("#A82623", "█"))         #front
    colored_logo = colored_logo.replace("▒",hex_to_rgb("#701715", "▒")) #bg
    
    print(colored_logo)
    csprint("От - Wl13Proger9\n")


    m = menu(
            items = [
                        'Запустить игру',
                        'Параметры',
                        'Выйти',
                    ],

            auto_clear   = False,
            bottom_input = True,
            )

    
    main_menu = m.vertical(
                            desc=[
                                    'Открыть игру',
                                    'Изменить настройки',
                                    'Выйти',
                                ]
                        )

    match main_menu['selected']:
        case 1: start_game()
        case 2: params()
        case 3: cli_exit()

        case _: on_nothing()



if __name__ == "__main__":
    main()
'''
by Wl13Proger9                                                                                                                                                                                                                                                                                                     
'''

import os
import sys

import msvcrt
import ctypes

import time
import re

from PIL import Image




def colored(hex_color: str) -> str:
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple( int(hex_color[i:i+2], 16) for i in (0, 2, 4) )

        return f"\033[38;2;{r};{g};{b}m"
    except Exception as e: return e


def csprint(text: str,   
            delay: float = 0.0125, 

            user_input: bool = False,
            anim: bool = True) -> str:
    try:
        if anim:
            buffer = []

            for char in text:
                buffer.append(char)
                print(f"\r{''.join(buffer)}", end="", flush=True)
                time.sleep(delay)

            buffer = []
            if user_input:
                try:    return input(''.join(buffer))
                except (Exception, KeyboardInterrupt):return ''
    

        else:
            if user_input:
                try:    return input(text)
                except (Exception, KeyboardInterrupt):return ''


            print(text)
    except: print(text)


  
     


class menu:
    def __init__(
                self,
                user_keys:dict = {
                                  'up':   'H',
                                  'down': 'P',
                                  'left': 'K',
                                  'right':'M',
                                },

                items: list[str] = ["..."],
                auto_selected: int = 0,

                auto_clear: bool = True,     
                bottom_input: bool = False,

                ctrl_c: bool = True,    
                menu_anim: bool = True, 

                hide_cursor: bool = True,
                choose_char: str = ">"  
                ):
        
        kernel32 = ctypes.windll.kernel32
        hStdOut = kernel32.GetStdHandle(-11)  
        mode = ctypes.c_uint()
        
        if kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode)):
            kernel32.SetConsoleMode(hStdOut, mode.value | 0x0004)  


        def get_cursor_position() -> int:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 5)

            
            sys.stdout.write("\033[6n")
            sys.stdout.flush()

            resp = ''
            start = time.time()
            timeout = 0.5  
            while True:
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    resp += ch
                    if ch == 'R':break
                elif time.time() - start > timeout:break


            m = re.match(r'\x1b\[(\d+);(\d+)R', resp)
            if m:return int(m[1])  
                    
        def move_cursor(x: int = 0, y: int = 0) -> None:
            print(f"\033[{y};{x}H", end="")

        def clear_line() -> None:
            print("\033[K", end="") 

        def cursor(code: int = 0) -> None:
            if code == 0:print('\033[?25l',end="", flush=True) #Hide
            else:        print('\033[?25h',end="", flush=True) #Show

        self.cursor = cursor
        self.clear_line = clear_line
        self.move_cursor = move_cursor
        self.get_cursor_position = get_cursor_position

        self.user_keys = user_keys
        self.menu_items = items

        self.auto_selected = auto_selected
        self.auto_clear = auto_clear

        self.bottom_input = bottom_input
        self.ctrl_c = ctrl_c

        self.terminal_height = os.get_terminal_size().columns
        self.terminal_width = os.get_terminal_size().lines

        self.menu_anim = menu_anim
        self.hide_cursor = hide_cursor

        self.choose_char = choose_char
        

    def vertical(self, margin_left: int = 0, width: int = 15, desc: bool = False) -> dict:
        #Проверяет нужно ли отображать описание меню
        def menu_desc(bottom_text = desc) -> bool:
            if not isinstance(bottom_text, bool) or bottom_text == True:
                return True
            return False

        #Авто очистка экрана
        if self.auto_clear == True:
            os.system('cls' if os.name == 'nt' else 'clear')

        #Прячем курсор
        if self.hide_cursor:self.cursor(0)

        #Позиция курсора
        menu_top_line = self.get_cursor_position() 

        #Автовыбор пункта в меню
        if self.auto_selected + 1 > len(self.menu_items):self.auto_selected = len(self.menu_items)-1

        #Переменные пользовательского ввода
        user_input = ''
        input_line = menu_top_line + len(self.menu_items)

        #Основной цикл
        try:
            FIRST_ANIM_SHOW  = self.menu_anim

            while True:
                #Отрисовка Меню
                for i, item in enumerate(self.menu_items):
                    self.move_cursor(1, menu_top_line + i)   # Перенос курсора для отрисовки
                    self.clear_line()                        # Сброс цвета
                                    
                    current_delay = 0.00625 / (2**i) if i < 5 else 0 # Понижение скорости отрисовки
                                    #0.0125

                    if i == self.auto_selected:#Выделенный элемент
                        max_width = max(len(i) for i in self.menu_items) - len(item) + width
                        
                        csprint(f"{' '*margin_left}\033[7;1m {self.choose_char} {item} {' '*max_width}\033[0m",
                                anim=FIRST_ANIM_SHOW,
                                delay=current_delay)  
                            
                    else: #Остальные, не выделенные элементы
                        csprint(f"{' '*margin_left}  {item}{' '*width}",
                                                anim=FIRST_ANIM_SHOW,
                                                delay=current_delay)    

                                        
                FIRST_ANIM_SHOW = False


                #Отрисовка описания
                if menu_desc(desc):
                    desc_y_pos = menu_top_line + len(self.menu_items) + 1 
                    #Координата отрисовки меню. К тому же прибавляется один пробел для читаемости


                    for offset in range(4): 
                        self.move_cursor(1, desc_y_pos + offset)
                        self.clear_line()

                    self.move_cursor(1, desc_y_pos)
                    
                    try:   print(f"\033[3m{desc[self.auto_selected]}\033[0m", end="", flush=True)    
                    except:print(f"\033[90mОписание отсутствует\033[0m", end="", flush=True)
                                                
                
                #Отрисовка пользовательского ввода
                if self.bottom_input == True:
                    self.cursor(1)                  #Показать курсор
                    self.move_cursor(1, input_line) #Перенести курсор вниз для отрисовки
                    self.clear_line()               #Сбросить цвета

                    print(f"{user_input}", end="")  #Вывести пользовательский ввод
                    sys.stdout.flush()              

                
                #Считывание клавиш
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    #\x00 = Функциональные клавиши
                    #\xe0 = Навигационные клавиши
                    key = msvcrt.getch()
                                    
                
                if key == f"{self.user_keys['up']}".encode():       #Up Arrow
                    self.auto_selected = (self.auto_selected - 1) % len(self.menu_items)  

                elif key == f"{self.user_keys['down']}".encode():   #Down Arrow
                    self.auto_selected = (self.auto_selected + 1) % len(self.menu_items)

                elif key == b'\r':                                  #Enter   
                    if not user_input.strip() == "":
                        print()    #Лишний пробел если есть user_input
                    self.cursor(1) #Показать курсор
                    print()        #Лишний пробел на всякий случай

                    return {"selected": self.auto_selected+1,"user_input": user_input} 
                                
                elif key == b'\x08':                                #Backspace
                    if self.bottom_input == True:
                        user_input = user_input[:-1]
                        #Работает только если user_input == True

                elif key == b'\x03':                                #Ctrl+C             
                    if self.ctrl_c == True:
                        self.cursor(1) #Показать курсор
                        return {"selected": '', "user_input": ''} 
                    
                else:
                    if self.bottom_input == True:
                        self.cursor(1) #Показать курсор
                        try:ch = key.decode("utf-8")
                        except UnicodeDecodeError:ch = ""
                        if ch and ch.isprintable():user_input += ch




        #На случай ошибки
        except Exception as e: 
            self.cursor(1)
            self.move_cursor(1, input_line + 2)
            return e
                
            

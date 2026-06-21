# todo 

"""
картинка на фоні
Поле для введення нікнейму і кнопка Продовжити
кнопка виходу
"""

from customtkinter import *
from PIL import *
from setting import *

class NicknameMenu(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{NICKNAME_MENU_WIDTH}x{NICKNAME_MENU_HEIGHT}")
        self.title("Welcome to the game")


nickname_menu = NicknameMenu()
nickname_menu.mainloop()
        

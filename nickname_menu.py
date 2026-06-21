# todo 

"""
картинка на фоні
Поле для введення нікнейму і кнопка Продовжити
кнопка виходу
"""

from customtkinter import *
from PIL import Image
from setting import *

class NicknameMenu(CTk):

    username = ""

    def __init__(self):
        super().__init__()
        self.geometry(f"{NICKNAME_MENU_WIDTH}x{NICKNAME_MENU_HEIGHT}")
        self.title("Welcome to the game")
        self.resizable(False, False)

        self.image_label = CTkLabel(self, 
                                    image = 
                                    CTkImage(
                                        light_image=Image.open(nickname_menu_image_bg),
                                        size = (
                                            NICKNAME_MENU_WIDTH, 
                                            NICKNAME_MENU_HEIGHT
                                        )),
                                        text = ""
                                    )
        self.image_label.place(x = 0, y = 0)



        self.frame = CTkFrame(self, 
                              width = 400, 
                              height = 600, 
                              fg_color="#00245e", 
                              bg_color="#00245e")
        self.frame.pack_propagate(False)
        self.frame.pack(pady = 110)


        self.title = CTkLabel(self.frame, 
                              text="Welcome to the game!", 
                              font = title_font
        )
        self.title.pack(pady = 5)

        self.entry = CTkEntry(self.frame, 
                              placeholder_text="Enter your nickname ...",
                              width = 300,
                              height = 50,
                              fg_color="white",
                              font = entry_font,
                              text_color="black")
        self.entry.pack(pady = 10)

        self.play_button = CTkButton(self.frame,
                                    text = "Let's play",
                                    width = 300,
                                    height = 50,
                                    fg_color="white",
                                    font = entry_font,
                                    text_color = "black",
                                    hover_color="orange",
                                    command=self.get_nickname
                                    )
        self.play_button.pack()

    def get_nickname(self):
        self.username = self.entry.get().strip()
        print(self.username)
        # перехід до екрану гри
        return self.username



nickname_menu = NicknameMenu()
nickname_menu.mainloop()
        

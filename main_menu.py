# Кнопка виходу Кнопка грати Кнопкаи налаштувань Фон
#!!! Додати welcome user
from customtkinter import *
from PIL import Image
from setting import *
from play_menu import PlayMenu
from settings_menu import SettMenu

class MainMenu(CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username # ? Для майбутнього використання
        self.title("Main Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open(main_menu_image_bg)
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)

        # !! Додала контейнер, щоб згрупувати елементи
        self.frame = CTkFrame(self, 
                              width = 400, 
                              height = 600, 
                              fg_color="transparent",
                              bg_color="transparent")
        self.frame.pack_propagate(False)
        self.frame.pack(pady = 110)

        self.lbl_title = CTkLabel(self.frame, text = f"Welcome, {self.username}", font = title_font)
        self.lbl_title.pack(pady = 10)

        # Buttons
        self.play_button = CTkButton(self.frame, text="Play", command=self.play_game, width=100, height=50, fg_color="darkblue", hover_color="purple")
        self.exit_button = CTkButton(self.frame, command=self.exit_game, width=100, height=50, text="Exit", fg_color="darkblue", hover_color="purple")
        self.settings_button = CTkButton(self.frame, command=self.open_settings, width=100, height=50, text="Settings",fg_color="darkblue",  hover_color="purple")
        #Draw buttons
        self.play_button.pack(pady = 30)
        self.settings_button.pack()
        self.exit_button.pack(pady = 30)


        # Function for buttons
    def play_game(self):
        print("Play button clicked")
        self.destroy()  # Закриваємо головне меню перед відкриттям PlayMenu
        play_menu = PlayMenu()
        play_menu.mainloop()
    def exit_game(self):
        quit()  # Закриваємо програму при натисканні кнопки виходу
    def open_settings(self):
        self.destroy()  # Закриваємо головне меню перед відкриттям SettMenu
        sett_menu = SettMenu()
        sett_menu.mainloop()
        print("Settings button clicked")
    

# main_menu = MainMenu("Player1")
# main_menu.mainloop()
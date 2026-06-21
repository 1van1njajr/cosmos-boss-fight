# Кнопка виходу Кнопка грати Кнопкаи налаштувань Фон
#!!! Додати welcome user
from customtkinter import *
from PIL import Image
class MainMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Images
        self.exit_image = Image.open(r"assets\img\backgrounds\exit_button.jpg")
        self.exit_button_image = CTkImage(self.exit_image, size=(100, 50))

        self.settings_image = Image.open(r"assets\img\backgrounds\settings.jpg")
        self.settings_button_image = CTkImage(self.settings_image, size=(100, 50))

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\main_menu_bg.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)

        # Buttons
        self.play_button = CTkButton(self, text="Play", command=self.play_game, width=100, height=50)
        self.exit_button = CTkButton(self, image=self.exit_button_image, command=self.exit_game, width=100, height=50, text="", bg_color="transparent", fg_color="transparent", hover_color="grey")
        self.settings_button = CTkButton(self, image=self.settings_button_image, command=self.open_settings, width=100, height=50, text="", bg_color="transparent", fg_color="transparent", hover_color="grey")
        #Draw buttons
        self.play_button.place(x=450, y=250)
        self.exit_button.place(x=440, y=390)
        self.settings_button.place(x=440, y=320)


        # Function for buttons
    def play_game(self):
        print("Play button clicked")
    def exit_game(self):
        quit()
    def open_settings(self):
        print("Settings button clicked")

main_menu = MainMenu()
main_menu.mainloop()

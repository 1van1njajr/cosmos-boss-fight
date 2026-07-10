from customtkinter import *
from PIL import Image
from setting import *
class SettMenu(CTk):
    def __init__(self, username):
        super().__init__()
        self.title("Settings Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        self.username = username

        # Background
        self.bg_image = Image.open(settings_menu_image_bg)
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)
        # Buttons
        self.back_button = CTkButton(self, text="Back", width=100, height=50, command=self.go_back)
        self.back_button.place(x=450, y=300)
        # Functions for buttons
    def go_back(self):
        from ui_main_menu import MainMenu
        self.destroy()
        main_menu = MainMenu(self.username)
        main_menu.mainloop()


# sett_menu = SettMenu()
# sett_menu.mainloop()
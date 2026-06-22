from customtkinter import *
from PIL import Image
from setting import *
class SettMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Settings Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\nickname_menu_bg.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)

# sett_menu = SettMenu()
# sett_menu.mainloop()
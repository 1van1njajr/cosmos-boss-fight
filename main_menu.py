# Кнопка виходу Кнопка грати Кнопкаи налаштувань Фон
from customtkinter import *
from PIL import Image
class MainMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("800x600")
        self.configure(bg="black")

        self.bg_image = Image.open("background.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(800, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0)

from customtkinter import *
from PIL import Image
from setting import *
from join_lobby_menu import JoinLobbyMenu
from create_lobby_menu import CreateLobbyMenu
class PlayMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Play Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)
        # Images
        self.create_lobby_button_image = Image.open(r"assets\img\backgrounds\create_lobby_button.png")
        self.create_lobby_button_image = CTkImage(self.create_lobby_button_image, size=(200, 140))
        self.join_lobby_button_image = Image.open(r"assets\img\backgrounds\join_lobby_button.png")
        self.join_lobby_button_photo = CTkImage(self.join_lobby_button_image, size=(200, 140))

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\play_menu_bg.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)

# play_menu = PlayMenu()
# play_menu.mainloop()
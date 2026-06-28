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
        # self.create_lobby_button_image = Image.open(r"assets\img\backgrounds\create_lobby_button.png")
        # self.create_lobby_button_image = CTkImage(self.create_lobby_button_image, size=(100, 50))
        self.create_lobby_button_image = Image.open(r"assets\img\backgrounds\create_lobby_button.png")
        self.create_lobby_button_image = CTkImage(self.create_lobby_button_image, size=(200, 140))
        self.join_lobby_button_image = Image.open(r"assets\img\backgrounds\join_lobby_button.png")
        self.join_lobby_button_photo = CTkImage(self.join_lobby_button_image, size=(200, 150))
        self.join_lobby_button_photo = CTkImage(self.join_lobby_button_image, size=(200, 140))

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\play_menu_bg.jpg")

        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)

        # Buttons
        self.create_lobby_button = CTkButton(self, command=self.create_lobby, width=100, height=50, text="Create Lobby", bg_color="blue", fg_color="blue")
        self.join_lobby_button = CTkButton(self, image=self.join_lobby_button_photo, command=self.join_lobby, width=200, height=150, text="", bg_color="blue", fg_color="blue")
        # Buttons   
        self.create_lobby_button = CTkButton(self,image = self.create_lobby_button_image, command=self.create_lobby, width=200, height=140, text="", bg_color="blue", fg_color="blue")
        self.join_lobby_button = CTkButton(self, image=self.join_lobby_button_photo, command=self.join_lobby, width=200, height=140, text="", bg_color="blue", fg_color="blue")
        # Draw buttons
        self.create_lobby_button.place(x=400, y=200)
        self.create_lobby_button.place(x=400, y=100)
        self.join_lobby_button.place(x=400, y=300)
        # Functions for buttons
    def create_lobby(self):
        self.destroy()  # Закриваємо PlayMenu перед відкриттям CreateLobbyMenu
        print("Create Lobby button clicked")
        create_lobby_menu = CreateLobbyMenu()
        create_lobby_menu.mainloop()
    def join_lobby(self):
        self.destroy()  # Закриваємо PlayMenu перед відкриттям JoinLobbyMenu
        join_lobby_menu = JoinLobbyMenu()
        join_lobby_menu.mainloop()
        print("Join Lobby button clicked")

# play_menu = PlayMenu()
# play_menu.mainloop()
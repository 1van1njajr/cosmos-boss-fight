from customtkinter import *
from PIL import Image
from setting import *
from final_moder_menu import FinalModerMenu
class CreateLobbyMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Create Lobby Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open(create_lobby_menu_image_bg)
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)
        # Buttons
        self.enter_port = CTkEntry(self, placeholder_text="Enter Port", width=200, height=40)
        self.enter_port.place(x=400, y=200)

        self.enter_host = CTkEntry(self, placeholder_text="Enter Host", width=200, height=40)
        self.enter_host.place(x=400, y=250)

        self.back_button = CTkButton(self, text="Back", command=self.go_back, width=100, height=50)
        self.back_button.place(x=450, y=300)

        self.create_button = CTkButton(self, text="Create", command=self.create_lobby, width=200, height=50)
        self.create_button.place(x=400, y=400)
        # Functions for buttons
    def go_back(self):
        from play_menu import PlayMenu

        self.destroy()  # Закриваємо CreateLobbyMenu перед відкриттям PlayMenu
        play_menu = PlayMenu()
        play_menu.mainloop()
    def create_lobby(self):
        port = self.enter_port.get()
        host = self.enter_host.get()
        self.destroy() # `Закриваємо CreateLobbyMenu перед відкриттям FinalModerMenu`
        print(f"Creating lobby with Port: {port}, Host: {host}")
        final_moder_menu = FinalModerMenu()
        final_moder_menu.mainloop()

# create_lobby_menu = CreateLobbyMenu()
# create_lobby_menu.mainloop()
from customtkinter import *
from PIL import Image
from setting import *
from final_player_menu import FinalPlayerMenu
class JoinLobbyMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Join Lobby Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\join_lobby_bg.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)
        # Buttons And Entries
        self.enter_port = CTkEntry(self, placeholder_text="Enter Port", width=200, height=40)
        self.enter_port.place(x=400, y=200)
        self.enter_host = CTkEntry(self, placeholder_text="Enter Host", width=200, height=40)
        self.enter_host.place(x=400, y=250)
        self.back_button = CTkButton(self, text="Back", command=self.go_back, width=100, height=50)
        self.back_button.place(x=450, y=300)
        self.join_button = CTkButton(self, text="Join", command=self.join_lobby, width=200, height=50)
        self.join_button.place(x=400, y=400)
        # Functions for buttons
    def go_back(self):
        from play_menu import PlayMenu

        self.destroy()  # Закриваємо JoinLobbyMenu перед відкриттям PlayMenu
        play_menu = PlayMenu()
        play_menu.mainloop()
    def join_lobby(self):
        self.destroy()  # Закриваємо JoinLobbyMenu перед відкриттям FinalPlayerMenu
        port = self.enter_port.get()
        host = self.enter_host.get()
        print(f"Joining lobby with Port: {port}, Host: {host}")
        final_player_menu = FinalPlayerMenu()
        final_player_menu.mainloop()

# join_lobby_menu = JoinLobbyMenu()
# join_lobby_menu.mainloop()
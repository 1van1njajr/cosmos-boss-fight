from customtkinter import *
from PIL import Image
from setting import *
class FinalPlayerMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Final Player Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open=(main_menu_image_bg)
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)
        # Buttons
        self.back_button = CTkButton(self, text="Back", command=self.go_back, width=100, height=50)
        self.back_button.place(x=450, y=300)
        # Functions for buttons
    def go_back(self):
        from join_lobby_menu import JoinLobbyMenu

        self.destroy()  # Закриваємо FinalPlayerMenu перед відкриттям JoinLobbyMenu
        join_lobby_menu = JoinLobbyMenu()
        join_lobby_menu.mainloop()
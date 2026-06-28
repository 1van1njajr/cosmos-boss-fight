from customtkinter import *
from PIL import Image
from setting import *
class FinalModerMenu(CTk):
    def __init__(self):
        super().__init__()
        self.title("Final Moder Menu")
        self.geometry("1000x600")
        self.configure(bg="black")
        self.resizable(False, False)

        # Background
        self.bg_image = Image.open(r"assets\img\backgrounds\final_moder_menu.jpg")
        self.bg_photo = CTkImage(self.bg_image, size=(1000, 600))
        self.bg_label = CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0)
        # Buttons
        self.back_button = CTkButton(self, text="Back", command=self.go_back, width=100, height=50)
        self.back_button.place(x=450, y=300)



        # Functions for buttons
    def go_back(self):
        from create_lobby_menu import CreateLobbyMenu

        self.destroy()  # Закриваємо FinalModerMenu перед відкриттям CreateLobbyMenu
        create_lobby_menu = CreateLobbyMenu()
        create_lobby_menu.mainloop()
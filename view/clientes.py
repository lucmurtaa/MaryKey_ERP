import customtkinter as ctk

class ClientsView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        title = ctk.CTkLabel(
            self.frame,
            text="Clientes",
            font=("Arial", 28, "bold")
        )
        title.grid(pady=20)
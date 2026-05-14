import customtkinter as ctk

class DashboardView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        title = ctk.CTkLabel(
            self.frame,
            text="Dashboard",
            font=("Arial", 28, "bold")
        )
        title.grid(pady=20)

        info = ctk.CTkLabel(
            self.frame,
            text="Bem-vindo ao ERP Mary Kay"
        )
        info.grid()
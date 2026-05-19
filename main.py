import customtkinter as ctk

from database.schema import create_tables
from view.login import LoginView

create_tables()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("ERP Mary Kay")
app.geometry("1200x700")

LoginView(app)

app.mainloop() 
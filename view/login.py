import customtkinter as ctk

from view.Main_window import MainWindow


class LoginView:

    def __init__(self, app):

        self.app = app

        self.frame = ctk.CTkFrame(app)
        self.frame.pack(expand=True)

        self.title = ctk.CTkLabel(
            self.frame,
            text="ERP Mary Kay",
            font=("Arial", 28, "bold")
        )
        self.title.pack(pady=20)

        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Usuário",
            width=250
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Senha",
            show="*",
            width=250
        )
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(
            self.frame,
            text="Entrar",
            command=self.login
        )
        self.login_button.pack(pady=20)

    def login(self):
        # Aqui você pode adicionar a lógica de autenticação
        # Por exemplo, verificar o nome de usuário e senha em um banco de dados

        # Se a autenticação for bem-sucedida, você pode abrir a janela principal
        self.frame.destroy()  # Fecha a tela de login
        MainWindow(self.app)  # Abre a janela principal
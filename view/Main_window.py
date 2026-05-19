import customtkinter as ctk
import view.dashboard as dashboard
import view.clientes as clientes
import view.produtos as produtos
import view.vendas as vendas
from view.clientes import ClientesView

from view.produtos import ProductsView
from view.vendas import VendasView

class MainWindow:
    def __init__(self, app):

        self.app = app
        self.container = ctk.CTkFrame(app)
        self.container.pack(fill="both", expand=True)

        #side bar
        self.side_bar = ctk.CTkFrame(self.container, width=200)
        self.side_bar.pack(side="left", fill="y")

         # ÁREA DE CONTEÚDO
        self.content = ctk.CTkFrame(self.container)
        self.content.pack(side="right", fill="both", expand=True)

        #botões do menu

        dashboard_btn = ctk.CTkButton(
            self.side_bar,
            text="Dashboard",
            command=self.show_dashboard
        )
        dashboard_btn.pack(pady=10)

        produtos_btn = ctk.CTkButton(
            self.side_bar,
            text="Produtos",
            command=self.carregar_products
        
        )
        produtos_btn.pack(pady=10)

        clientes_btn = ctk.CTkButton(
            self.side_bar,
            text="Clientes",
            command=self.carregar_clientes
        )
        clientes_btn.pack(pady=10)

        vendas_btn = ctk.CTkButton(
            self.side_bar,
            text="Vendas",
            command=self.carregar_vendas
        )
        vendas_btn.pack(pady=10)

        self.current_screen = None
        # TELA INICIAL
        self.show_dashboard()

    



    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        print("Exibindo dashboard")
        self.clear_content()
        view = dashboard.DashboardView(self.content)
        view.frame.pack(fill="both", expand=True)
        
    def carregar_products(self):
        print("Exibindo produtos")
        self.clear_content()
            
        view = ProductsView(self.content)
        view.frame.pack(fill="both", expand=True)

    def carregar_clientes(self):
        print("Exibindo clientes")
        self.clear_content()
            
        view = clientes.ClientesView(self.content)
        view.frame.pack(fill="both", expand=True)

    def carregar_vendas(self):
        print("Exibindo vendas")
        self.clear_content()

        view = VendasView(self.content)
        view.frame.pack(fill="both", expand=True)

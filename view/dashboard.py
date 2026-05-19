import customtkinter as ctk
from services.produto_service import ProductService
from services.cliente_service import ClienteService
from services.venda_service import VendaService


class DashboardView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self.frame,
            text="Dashboard",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=20)

        cards_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=20)


        total_clientes = ClienteService.total_clientes()
        total_produtos = ProductService.total_products()
        total_vendas = VendaService.total_vendas()
        faturamento = VendaService.total_faturamento()

        # CARDS
        

        self.create_card(
            cards_frame,
            "Clientes",
            total_clientes,
            0
        )
        self.create_card(
            cards_frame,
            "Produtos",
            total_produtos,
            1
        )
        self.create_card(
            cards_frame,
            "Vendas",
            total_vendas,
            2
        )
        self.create_card(
            cards_frame,
            "Faturamento",
            f"R$ {faturamento:.2f}",
            3
        )

        #criando a busca de vendas por cliente

        search_frame = ctk.CTkFrame(self.frame)
        search_frame.pack(fill="x", padx=20, pady=(10, 0))

        search_label = ctk.CTkLabel(
            search_frame,
            text="Buscar compras por cliente",
            font=("Arial", 18, "bold")
        )
        search_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

        self.client_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite o nome do cliente..."
        )
        self.client_search_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        search_button = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.buscar_compras_cliente
        )
        search_button.grid(row=1, column=1, padx=10, pady=10)

        search_frame.grid_columnconfigure(0, weight=1)

        results_title = ctk.CTkLabel(
            self.frame,
            text="Compras encontradas",
            font=("Arial", 18, "bold")
        )
        results_title.pack(anchor="w", padx=20, pady=(15, 0))

        self.compras_list = ctk.CTkScrollableFrame(self.frame)
        self.compras_list.pack(fill="both", expand=True, padx=20, pady=20)

        self.render_empty_state()

    def buscar_compras_cliente(self):
        term = self.client_search_entry.get().strip()

        self.clear_results()

        if not term:
            self.render_empty_state("Digite o nome de um cliente para buscar suas compras.")
            return

        vendas = VendaService.search_vendas_por_cliente(term)

        if not vendas:
            self.render_empty_state("Nenhuma compra encontrada para esse cliente.")
            return

        header = ctk.CTkFrame(self.compras_list)
        header.pack(fill="x", pady=(0, 8))

        for column, text, weight in [
            (0, "ID", 0),
            (1, "Cliente", 2),
            (2, "Produto", 2),
            (3, "Pagamento", 1),
            (4, "Total", 1),
            (5, "Data", 1)
        ]:
            label = ctk.CTkLabel(header, text=text, font=("Arial", 14, "bold"))
            label.grid(row=0, column=column, padx=10, pady=8, sticky="w")
            header.grid_columnconfigure(column, weight=weight)

        for venda in vendas:
            row = ctk.CTkFrame(self.compras_list)
            row.pack(fill="x", pady=4)

            values = [
                venda[0],
                venda[1],
                venda[2],
                venda[3],
                f"R$ {venda[4]:.2f}",
                venda[5]
            ]

            weights = [0, 2, 2, 1, 1, 1]
            for column, value in enumerate(values):
                label = ctk.CTkLabel(row, text=str(value), anchor="w")
                label.grid(row=0, column=column, padx=10, pady=8, sticky="w")
                row.grid_columnconfigure(column, weight=weights[column])

    def clear_results(self):
        for widget in self.compras_list.winfo_children():
            widget.destroy()

    def render_empty_state(self, message="Nenhuma busca realizada ainda."):
        self.clear_results()

        empty_label = ctk.CTkLabel(
            self.compras_list,
            text=message,
            font=("Arial", 14)
        )
        empty_label.pack(pady=20)

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            width=200,
            height=120
        )

        card.grid(
            row=0,
            column=column,
            padx=15,
            pady=20
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18)
        )
        title_label.pack(pady=(20, 10))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold")
        )
        value_label.pack()
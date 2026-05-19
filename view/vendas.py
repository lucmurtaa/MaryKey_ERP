import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

from services.cliente_service import ClienteService
from services.produto_service import ProductService
from services.venda_service import VendaService


class VendasView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self.frame,
            text="Vendas",
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        form_frame = ctk.CTkFrame(self.frame)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(form_frame, text="Cliente").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(form_frame, text="Produto").grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(form_frame, text="Forma de pagamento").grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")

        self.cliente_var = ctk.StringVar()
        self.produto_var = ctk.StringVar()
        self.pagamento_var = ctk.StringVar()

        self.cliente_menu = ctk.CTkComboBox(form_frame, variable=self.cliente_var, values=[])
        self.cliente_menu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.produto_menu = ctk.CTkComboBox(form_frame, variable=self.produto_var, values=[])
        self.produto_menu.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.pagamento_menu = ctk.CTkComboBox(
            form_frame,
            variable=self.pagamento_var,
            values=["Pix", "Cartão", "Dinheiro", "Transferência"]
        )
        self.pagamento_menu.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="ew")

        cadastrar_button = ctk.CTkButton(form_frame, text="Registrar venda", command=self.registrar_venda)
        cadastrar_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        self.vendas_table = ttk.Treeview(
            self.frame,
            columns=("ID", "Cliente", "Produto", "Pagamento", "Total", "Data"),
            show="headings"
        )
        for coluna, titulo in [
            ("ID", "ID"),
            ("Cliente", "Cliente"),
            ("Produto", "Produto"),
            ("Pagamento", "Pagamento"),
            ("Total", "Total"),
            ("Data", "Data")
        ]:
            self.vendas_table.heading(coluna, text=titulo)

        self.vendas_table.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.clientes_map = {}
        self.produtos_map = {}

        self.load_combos()
        self.load_vendas()

    def load_combos(self):
        clientes = ClienteService.get_clientes()
        produtos = ProductService.get_products()

        cliente_values = []
        for cliente in clientes:
            label = f"{cliente[0]} - {cliente[1]}"
            cliente_values.append(label)
            self.clientes_map[label] = cliente[0]

        produto_values = []
        for produto in produtos:
            label = f"{produto[0]} - {produto[1]}"
            produto_values.append(label)
            self.produtos_map[label] = produto[0]

        self.cliente_menu.configure(values=cliente_values)
        self.produto_menu.configure(values=produto_values)

        if cliente_values:
            self.cliente_var.set(cliente_values[0])
        if produto_values:
            self.produto_var.set(produto_values[0])
        self.pagamento_var.set("Pix")

    def registrar_venda(self):
        cliente_label = self.cliente_var.get().strip()
        produto_label = self.produto_var.get().strip()
        forma_pagamento = self.pagamento_var.get().strip()

        cliente_id = self.clientes_map.get(cliente_label)
        produto_id = self.produtos_map.get(produto_label)

        success, message = VendaService.registrar_venda(cliente_id, produto_id, forma_pagamento)

        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_vendas()
        else:
            messagebox.showerror("Erro", message)

    def load_vendas(self):
        for item in self.vendas_table.get_children():
            self.vendas_table.delete(item)

        vendas = VendaService.get_vendas()
        for venda in vendas:
            self.vendas_table.insert("", "end", values=venda)
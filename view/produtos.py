import customtkinter as ctk
from tkinter import messagebox

from tkinter import ttk
from tkcalendar import DateEntry


from services.produto_service import ProductService


class ProductsView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        
        title = ctk.CTkLabel(
            self.frame,
            text="Produtos",
            font=("Arial", 28, "bold"),
            width=250
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        #FORMULARIOS    

        from_frame = ctk.CTkFrame(self.frame)
        from_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        from_frame.grid_columnconfigure(0, weight=1)
        from_frame.grid_columnconfigure(1, weight=1)
        from_frame.grid_columnconfigure(2, weight=1)

        # NOME
        ctk.CTkLabel(from_frame, text="Nome do Produto").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.name_entry = ctk.CTkEntry(from_frame, placeholder_text="Nome do Produto")
        self.name_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        # PREÇO DE COMPRA / VENDA / VALIDADE
        ctk.CTkLabel(from_frame, text="Preço de Compra").grid(row=2, column=0, padx=10, pady=(0, 0), sticky="w")
        ctk.CTkLabel(from_frame, text="Preço de Venda").grid(row=2, column=1, padx=10, pady=(0, 0), sticky="w")
        ctk.CTkLabel(from_frame, text="Validade").grid(row=2, column=2, padx=10, pady=(0, 0), sticky="w")

        self.preco_compra_entry = ctk.CTkEntry(from_frame, placeholder_text="Preço de Compra")
        self.preco_compra_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.preco_venda_entry = ctk.CTkEntry(from_frame, placeholder_text="Preço de Venda")
        self.preco_venda_entry.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.validade_entry = DateEntry(from_frame)
        self.validade_entry.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="ew")

        # BOTÃO DE CADASTRAR
        cadastrar_button = ctk.CTkButton(from_frame, text="Cadastrar", command=self.cadastrar_products)
        cadastrar_button.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        # BOTÃO DE EDITAR
        edit_button = ctk.CTkButton(from_frame, text="Editar", command=self.edit_products)
        edit_button.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        # BOTÃO DE deletar
        delete_button = ctk.CTkButton(from_frame, text="Deletar", command=self.delete_products)
        delete_button.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        #TABELA DE PRODUTOS
        self.produtos_table = ttk.Treeview(self.frame, 
                                           columns=("ID", "Nome", "Preço de Compra", "Preço de Venda", "Validade"), 
                                           show="headings"
                                           )
        self.produtos_table.heading("ID", text="ID")
        self.produtos_table.heading("Nome", text="Nome")
        self.produtos_table.heading("Preço de Compra", text="Preço de Compra")
        self.produtos_table.heading("Preço de Venda", text="Preço de Venda")
        self.produtos_table.heading("Validade", text="Validade")
        self.produtos_table.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.load_products()

    def cadastrar_products(self):
        name = self.name_entry.get().strip()
        preco_compra = self.preco_compra_entry.get().strip()
        preco_venda = self.preco_venda_entry.get().strip()
        validade = self.validade_entry.get_date()

        if not name or not preco_compra or not preco_venda:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            preco_compra = float(preco_compra)
            preco_venda = float(preco_venda)
        except ValueError:
            messagebox.showerror("Erro", "Preço de compra e venda devem ser números.")
            return

        ProductService.cadastrar_products(name, preco_compra, preco_venda, validade)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        self.limpar_campos()
        self.load_products()

    def load_products(self):
        for item in self.produtos_table.get_children():
            self.produtos_table.delete(item)

        produtos = ProductService.get_products()
        for produto in produtos:
            self.produtos_table.insert("", "end", values=produto)

    def edit_products(self):
        selected_item = self.produtos_table.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um produto para editar.")
            return

        produto_id = self.produtos_table.item(selected_item[0])["values"][0]
        name = self.name_entry.get().strip()
        preco_compra = self.preco_compra_entry.get().strip()
        preco_venda = self.preco_venda_entry.get().strip()
        validade = self.validade_entry.get_date()
        success, message = ProductService.edit_products(produto_id, name, preco_compra, preco_venda, validade)

        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_products()
        else:
            messagebox.showerror("Erro", message)


        
    def delete_products(self):
        selected_item = self.produtos_table.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um produto para deletar.")
            return

        produto_id = self.produtos_table.item(selected_item[0])["values"][0]
        success, message = ProductService.delete_products(produto_id)

        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_products()
        else:
            messagebox.showerror("Erro", message)

    def limpar_campos(self):
        self.name_entry.delete(0, "end")
        self.preco_compra_entry.delete(0, "end")
        self.preco_venda_entry.delete(0, "end")
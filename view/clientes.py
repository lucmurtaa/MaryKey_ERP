import customtkinter as ctk
from tkinter import messagebox

from tkinter import ttk
from tkcalendar import DateEntry

from services.cliente_service import ClienteService


class ClientesView:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        
        title = ctk.CTkLabel(
            self.frame,
            text="Clientes",
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
        ctk.CTkLabel(from_frame, text="Nome do Cliente").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.name_entry = ctk.CTkEntry(from_frame, placeholder_text="Nome do Cliente")
        self.name_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        # TELEFONE
        ctk.CTkLabel(from_frame, text="Telefone").grid(row=2, column=0, padx=10, pady=(0, 0), sticky="w")
        self.telefone_entry = ctk.CTkEntry(from_frame, placeholder_text="Telefone")
        self.telefone_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # EMAIL
        ctk.CTkLabel(from_frame, text="Email").grid(row=2, column=1, padx=10, pady=(0, 0), sticky="w")
        self.email_entry = ctk.CTkEntry(from_frame, placeholder_text="Email")
        self.email_entry.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="ew")

        # BOTÃO DE CADASTRAR
        cadastrar_button = ctk.CTkButton(from_frame, text="Cadastrar", command=self.cadastrar_clientes)
        cadastrar_button.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        # BOTÃO DE EDITAR
        edit_button = ctk.CTkButton(from_frame, text="Editar", command=self.edit_clientes)
        edit_button.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        # BOTÃO DE deletar
        delete_button = ctk.CTkButton(from_frame, text="Deletar", command=self.delete_clientes)
        delete_button.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

        # CAMPO DE PESQUISA
        self.search_entry = ctk.CTkEntry(self.frame,placeholder_text="Pesquisar cliente...", width=200)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>",self.search_clientes)      

        #TABELA DE CLIENTES
        self.clientes_table = ttk.Treeview(self.frame, 
                                           columns=("ID", "Nome", "Telefone", "Email"), 
                                           show="headings"
                                           )
        self.clientes_table.heading("ID", text="ID")
        self.clientes_table.heading("Nome", text="Nome")
        self.clientes_table.heading("Telefone", text="Telefone")
        self.clientes_table.heading("Email", text="Email")
        self.clientes_table.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.load_clientes()

    def cadastrar_clientes(self):
        name = self.name_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not telefone or not email:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return


        ClienteService.cadastrar_clientes(name, telefone, email)
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        self.limpar_campos()
        self.load_clientes()

    def load_clientes(self):
        for item in self.clientes_table.get_children():
            self.clientes_table.delete(item)

        clientes = ClienteService.get_clientes()
        for cliente in clientes:
            self.clientes_table.insert("", "end", values=cliente)

    def edit_clientes(self):
        selected_item = self.clientes_table.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um cliente para editar.")
            return

        cliente_id = self.clientes_table.item(selected_item[0])["values"][0]
        name = self.name_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()
        success, message = ClienteService.edit_clientes(cliente_id, name, telefone, email)

        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_clientes()
        else:
            messagebox.showerror("Erro", message)


        
    def delete_clientes(self):
        selected_item = self.clientes_table.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um cliente para deletar.")
            return

        cliente_id = self.clientes_table.item(selected_item[0])["values"][0]
        success, message = ClienteService.delete_clientes(cliente_id)

        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_clientes()
        else:
            messagebox.showerror("Erro", message)

    def limpar_campos(self):
        self.name_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

    def search_clientes(self, event):

        search_term = self.search_entry.get().lower()

        # LIMPA TABELA
        for item in self.clientes_table.get_children():
            self.clientes_table.delete(item)

        # BUSCA TODOS CLIENTES
        clientes = ClienteService.get_clientes()

        # FILTRA
        filtered_clientes = []

        for cliente in clientes:

            cliente_name = cliente[1].lower()

            if search_term in cliente_name:

                filtered_clientes.append(cliente)

        # REINSERE NA TABELA
        for cliente in filtered_clientes:
            self.clientes_table.insert(
                "",
                "end",
                values=cliente
            )
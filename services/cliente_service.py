from database.connection import connect_BD



class ClienteService:
    @staticmethod
    def cadastrar_clientes(name, telefone, email):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (name, telefone, email) VALUES(?, ?, ?)",
            (name, telefone, email)
        )
        conn.commit()
        conn.close()


    @staticmethod
    def get_clientes():
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clientes = cursor.fetchall()
        conn.close()

        return clientes

    @staticmethod
    def edit_clientes(cliente_id, name, telefone, email):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET name = ?, telefone = ?, email = ? WHERE id = ?",
            (name, telefone, email, cliente_id)
        )
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return True, "CLIENTE ATUALIZADO COM SUCESSO"

        return False, "CLIENTE NÃO ENCONTRADO"
    
    @staticmethod
    def delete_clientes(cliente_id):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (cliente_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return True, "CLIENTE DELETADO COM SUCESSO"
    
        return False, "CLIENTE NÃO ENCONTRADO"
    
    @staticmethod
    def search_clients(term):

        conn = connect_BD()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM clients
        WHERE name LIKE ?
        """, (f"%{term}%",))

        clients = cursor.fetchall()

        conn.close()

        return clients

    @staticmethod
    def total_clientes():
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients")
        total = cursor.fetchone()[0]
        conn.close()

        return total
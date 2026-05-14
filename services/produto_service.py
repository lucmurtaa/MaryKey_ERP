from database.connection import connect_BD 

class ProductService:
    @staticmethod
    def cadastrar_products(
        name,
        preco_compra,
        preco_venda,
        validade   
    ):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, preco_compra, preco_venda, validade) VALUES(?, ?, ?, ?)",
            (name, preco_compra, preco_venda, validade)
        )
        conn.commit()
        conn.close()


    @staticmethod
    def get_products():
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        produtos = cursor.fetchall()
        conn.close()
        
        return produtos 
    
    @staticmethod
    def edit_products(produto_id, name, preco_compra, preco_venda, validade):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name = ?, preco_compra = ?, preco_venda = ?, validade = ? WHERE id = ?",
            (name, preco_compra, preco_venda, validade, produto_id)
        )
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return True, "PRODUTO ATUALIZADO COM SUCESSO"

        return False, "PRODUTO NÃO ENCONTRADO"


    
    @staticmethod
    def delete_products(produto_id):
        conn = connect_BD()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (produto_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return True, "PRODUTO DELETADO COM SUCESSO"
    
        return False, "PRODUTO NÃO ENCONTRADO"
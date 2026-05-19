from datetime import date

from database.connection import connect_BD


class VendaService:

	@staticmethod
	def registrar_venda(cliente_id, produto_id, forma_pagamento):
		if not cliente_id or not produto_id or not forma_pagamento:
			return False, "Preencha cliente, produto e forma de pagamento."

		conn = connect_BD()
		cursor = conn.cursor()

		cursor.execute(
			"SELECT preco_venda FROM products WHERE id = ?",
			(produto_id,)
		)
		product = cursor.fetchone()

		if not product:
			conn.close()
			return False, "Produto não encontrado."

		total = product[0]
		data_venda = date.today().isoformat()

		cursor.execute(
			"""
			INSERT INTO vendas (client_id, product_id, total, forma_pagamento, data_venda)
			VALUES (?, ?, ?, ?, ?)
			""",
			(cliente_id, produto_id, total, forma_pagamento, data_venda)
		)

		conn.commit()
		conn.close()

		return True, "Venda registrada com sucesso."

	@staticmethod
	def get_vendas():
		conn = connect_BD()
		cursor = conn.cursor()

		cursor.execute(
			"""
			SELECT
				v.id,
				c.name,
				p.name,
				v.forma_pagamento,
				v.total,
				v.data_venda
			FROM vendas v
			LEFT JOIN clients c ON c.id = v.client_id
			LEFT JOIN products p ON p.id = v.product_id
			ORDER BY v.id DESC
			"""
		)

		vendas = cursor.fetchall()
		conn.close()

		return vendas

	@staticmethod
	def total_vendas():
		conn = connect_BD()
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM vendas")
		total = cursor.fetchone()[0]
		conn.close()

		return total

	@staticmethod
	def total_faturamento():
		conn = connect_BD()
		cursor = conn.cursor()
		cursor.execute("SELECT COALESCE(SUM(total), 0) FROM vendas")
		total = cursor.fetchone()[0]
		conn.close()

		return total

	@staticmethod
	def search_vendas_por_cliente(term):
		conn = connect_BD()
		cursor = conn.cursor()

		cursor.execute(
			"""
			SELECT
				v.id,
				c.name,
				p.name,
				v.forma_pagamento,
				v.total,
				v.data_venda
			FROM vendas v
			LEFT JOIN clients c ON c.id = v.client_id
			LEFT JOIN products p ON p.id = v.product_id
			WHERE c.name LIKE ?
			ORDER BY v.id DESC
			""",
			(f"%{term}%",)
		)

		vendas = cursor.fetchall()
		conn.close()

		return vendas

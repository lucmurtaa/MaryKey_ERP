from database.connection import connect_BD as connect

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        preco_compra REAL,
        preco_venda REAL,
        validade DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        telefone TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        product_id INTEGER,
        total REAL,
        forma_pagamento TEXT,
        data_venda TEXT
    )
    """)

    cursor.execute("PRAGMA table_info(vendas)")
    vendas_columns = [column[1] for column in cursor.fetchall()]

    if "product_id" not in vendas_columns:
        cursor.execute("ALTER TABLE vendas ADD COLUMN product_id INTEGER")

    conn.commit()
    conn.close()

    
import sqlite3

def criar_banco_de_dados():
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS orcamentos
    ''')
    cursor.execute('''
        CREATE TABLE orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            data TEXT,
            nome_cliente TEXT,
            telefone TEXT
        )
    ''')
    conn.commit()
    conn.close()

criar_banco_de_dados()

import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
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


def adicionar_orcamento(descricao, valor, data, nome_cliente, telefone):
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orcamentos (descricao, valor, data, nome_cliente, telefone)
        VALUES (?, ?, ?, ?, ?)
    ''', (descricao, valor, data.strftime('%d/%m/%Y %H:%M:%S'), nome_cliente, telefone))
    conn.commit()
    conn.close()


def remover_orcamento(id):
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orcamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def consultar_orcamentos():
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orcamentos')
    orcamentos = cursor.fetchall()
    conn.close()
    return orcamentos


def obter_proximo_id():
    conn = sqlite3.connect('orcamentos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM orcamentos')
    max_id = cursor.fetchone()[0]
    conn.close()
    return (max_id + 1) if max_id else 1

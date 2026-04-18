import os
import sqlite3

class Database:
    def __init__(self):
        # Localiza a pasta onde este arquivo 'database.py' está salvo
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_banco = os.path.join(diretorio_atual, "scores.db")

        # Conecta usando o caminho completo
        self.conn = sqlite3.connect("scores.db")
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_score(self, name, score):
        query = "INSERT INTO scores (name, score) VALUES (?, ?)"
        self.conn.execute(query, (name, score))
        self.conn.commit()

    def get_top_scores(self, limit=5):
        query = "SELECT name, score FROM scores ORDER BY score DESC LIMIT ?"
        cursor = self.conn.execute(query, (limit,))
        return cursor.fetchall()
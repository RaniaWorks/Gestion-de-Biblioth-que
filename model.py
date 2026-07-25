# model.py
import sqlite3

class Model:
    def __init__(self, db_name="bibliotheque.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            auteur TEXT,
            annee INTEGER,
            genre TEXT
        )
        """)
        self.conn.commit()

    def ajouter_livre(self, titre, auteur, annee, genre):
        self.conn.execute(
            "INSERT INTO livres (titre, auteur, annee, genre) VALUES (?, ?, ?, ?)",
            (titre, auteur, annee, genre)
        )
        self.conn.commit()

    def tout_afficher(self):
        return self.conn.execute("SELECT * FROM livres").fetchall()

    def rechercher(self, critere, valeur):
        return self.conn.execute(
            f"SELECT * FROM livres WHERE {critere} LIKE ?",
            (f"%{valeur}%",)
        ).fetchall()

    def modifier(self, livre_id, titre, auteur, annee, genre):
        self.conn.execute(
            "UPDATE livres SET titre=?, auteur=?, annee=?, genre=? WHERE id=?",
            (titre, auteur, annee, genre, livre_id)
        )
        self.conn.commit()

    def supprimer(self, livre_id):
        self.conn.execute("DELETE FROM livres WHERE id=?", (livre_id,))
        self.conn.commit()

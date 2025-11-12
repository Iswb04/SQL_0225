import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path


# Detecta se está rodando como .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys._MEIPASS)  # pasta temporária
    EXEC_DIR = Path(os.path.dirname(sys.executable))  # onde está o .exe
else:
    ROOT_DIR = Path(__file__).resolve().parent
    EXEC_DIR = ROOT_DIR

# Usa o diretório do executável para achar o banco
DB_FILE = EXEC_DIR / 'db.sqleague'
TABLE_NAME = 'Champions'


class LeagueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("League of Legends - Champions Infos")
        self.geometry("750x500")
        self.configure(bg="#101820")

        print(f"[DEBUG] Banco de dados procurado em: {DB_FILE}")  # útil pra debug

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self,
            text="Banco de Campeões",
            font=("Arial", 18, "bold"),
            fg="#F2AA4C",
            bg="#101820"
        )
        title_label.pack(pady=15)

        # Frame de busca
        search_frame = tk.Frame(self, bg="#101820")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Buscar Campeão:", fg="white", bg="#101820").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.search_champion).pack(side=tk.LEFT)

        # Tabela
        self.tree = ttk.Treeview(
            self,
            columns=("id", "name", "title", "tags", "counters"),
            show="headings"
        )

        # Cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nome")
        self.tree.heading("title", text="Título")
        self.tree.heading("tags", text="Funções")
        self.tree.heading("counters", text="Counters")

        # Largura das colunas
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=120, anchor="w")
        self.tree.column("title", width=150, anchor="w")
        self.tree.column("tags", width=150, anchor="w")
        self.tree.column("counters", width=250, anchor="w")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Botão listar todos
        ttk.Button(self, text="Listar Todos", command=self.load_all).pack(pady=5)


    def search_champion(self):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showwarning("Aviso", "Digite o nome de um campeão para buscar.")
            return

        if not DB_FILE.exists():
            messagebox.showerror("Erro", f"Banco de dados não encontrado em:\n{DB_FILE}")
            return

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"SELECT id, name, title, tags, counters FROM {TABLE_NAME} WHERE name LIKE ?",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erro no Banco", f"Ocorreu um erro:\n{e}")
            connection.close()
            return

        connection.close()

        self.tree.delete(*self.tree.get_children())

        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        else:
            messagebox.showinfo("Resultado", "Nenhum campeão encontrado.")

    def load_all(self):
        if not DB_FILE.exists():
            messagebox.showerror("Erro", f"Banco de dados não encontrado em:\n{DB_FILE}")
            return

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(f"SELECT id, name, title, tags, counters FROM {TABLE_NAME}")
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erro no Banco", f"Ocorreu um erro:\n{e}")
            connection.close()
            return

        connection.close()

        self.tree.delete(*self.tree.get_children())

        for r in rows:
            self.tree.insert("", tk.END, values=r)


if __name__ == "__main__":
    app = LeagueApp()
    app.mainloop()

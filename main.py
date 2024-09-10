import sqlite3
from tkinter import *
from tkinter import messagebox

# Criação do banco de dados SQLite
def criar_banco():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS produtos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER, preco REAL)''')
    conn.commit()
    conn.close()

# Função para adicionar um produto
def adicionar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()

    if nome and quantidade and preco:
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        entry_nome.delete(0, END)
        entry_quantidade.delete(0, END)
        entry_preco.delete(0, END)
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para buscar um produto
def buscar_produto():
    nome = entry_buscar.get()
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos WHERE nome=?", (nome,))
    produto = c.fetchone()
    conn.close()
    
    if produto:
        messagebox.showinfo("Produto encontrado", f"Nome: {produto[1]}\nQuantidade: {produto[2]}\nPreço: R${produto[3]:.2f}")
    else:
        messagebox.showwarning("Erro", "Produto não encontrado.")

# Função para atualizar a quantidade de um produto
def atualizar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()

    if nome and quantidade:
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("UPDATE produtos SET quantidade=? WHERE nome=?", (quantidade, nome))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
        entry_nome.delete(0, END)
        entry_quantidade.delete(0, END)
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para gerar relatório
def gerar_relatorio():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()

    relatorio = ""
    for produto in produtos:
        try:
            preco = float(produto[3])  # Converter o preço para float
            relatorio += f"Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: R${preco:.2f}\n"
        except ValueError:
            relatorio += f"Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: Valor inválido\n"

    if relatorio:
        messagebox.showinfo("Relatório de Estoque", relatorio)
    else:
        messagebox.showwarning("Erro", "Nenhum produto encontrado.")

# Interface gráfica com Tkinter
root = Tk()
root.title("Sistema de Controle de Estoque")

# Widgets da interface
Label(root, text="Nome do Produto:").grid(row=0, column=0)
entry_nome = Entry(root)
entry_nome.grid(row=0, column=1)

Label(root, text="Quantidade:").grid(row=1, column=0)
entry_quantidade = Entry(root)
entry_quantidade.grid(row=1, column=1)

Label(root, text="Preço:").grid(row=2, column=0)
entry_preco = Entry(root)
entry_preco.grid(row=2, column=1)

Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=1)

Label(root, text="Buscar Produto:").grid(row=4, column=0)
entry_buscar = Entry(root)
entry_buscar.grid(row=4, column=1)
Button(root, text="Buscar", command=buscar_produto).grid(row=4, column=2)

Button(root, text="Atualizar Estoque", command=atualizar_produto).grid(row=5, column=1)
Button(root, text="Gerar Relatório", command=gerar_relatorio).grid(row=6, column=1)

# Inicializar banco de dados
criar_banco()

# Executar interface
root.mainloop()
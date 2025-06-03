import sqlite3

# Criamos ou conectamos ao banco de dados
con = sqlite3.connect("dados.db")

# Aqui nos criamos a tabela Livros
con.execute("CREATE TABLE livros(\
            id INTEGER PRIMARY KEY,\
            titulo TEXT,\
            autor TEXT,\
            editora TEXT,\
            ano_publicado INTEGER,\
            isbn TEXT,\
            quantidade_total INTEGER,\
            quantidade_disponivel INTEGER)")

#Aqui nos criamos a tabela Usuarios
con.execute("CREATE TABLE usuarios(\
            id INTEGER PRIMARY KEY,\
            nome TEXT,\
            sobrenome TEXT,\
            endereco TEXT,\
            email TEXT,\
            telefone TEXT)")

# Aqui nos criamos a Tabela Emprestimos
con.execute("CREATE TABLE emprestimos(\
            id INTEGER PRIMARY KEY,\
            id_livros INTEGER,\
            id_usuarios INTEGER,\
            data_emprestimo TEXT,\
            data_devolucao TEXT,\
            status TEXT DEFAULT 'aberto',\
            FOREIGN KEY(id_livros) REFERENCES livros(id),\
            FOREIGN KEY(id_usuarios) REFERENCES usuarios(id))")

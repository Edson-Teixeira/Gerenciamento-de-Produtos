import sqlite3

# Criamos ou conectamos ao banco de dados
con = sqlite3.connect("dados.db")
cur = con.cursor()

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

livros = [
    ("Dom Casmurro", "Machado de Assis", "Editora Globo", 1899, "9788520901903", 50, 50),
    ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "HarperCollins", 1943, "9788595081512", 50, 50),
    ("1984", "George Orwell", "Companhia das Letras", 1949, "9788535909551", 50, 50),
    ("O Hobbit", "J.R.R. Tolkien", "HarperCollins", 1937, "9788595084742", 50, 50),
    ("A Revolução dos Bichos", "George Orwell", "Companhia das Letras", 1945, "9788535914845", 50, 50)
]
cur.executemany("""
INSERT INTO livros (titulo, autor, editora, ano_publicado, isbn, quantidade_total, quantidade_disponivel)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", livros)

usuarios = [
    ("Ana", "Silva", "Rua das Flores, 123", "ana.silva@email.com", "(81) 98888-1111"),
    ("Bruno", "Souza", "Av. Brasil, 456", "bruno.souza@email.com", "(81) 98777-2222"),
    ("Carla", "Oliveira", "Rua Verde, 789", "carla.oliveira@email.com", "(81) 98666-3333"),
    ("Diego", "Santos", "Travessa Azul, 321", "diego.santos@email.com", "(81) 98555-4444"),
    ("Fernanda", "Pereira", "Rua Central, 654", "fernanda.pereira@email.com", "(81) 98444-5555")
]
cur.executemany("""
INSERT INTO usuarios (nome, sobrenome, endereco, email, telefone)
VALUES (?, ?, ?, ?, ?)
""", usuarios)

con.commit()
con.close()

# classe de livros
class Livro:
    def __init__(self, titulo, autor, editora, ano, isbn):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.isbn = isbn
# classe de usuarios
class Usuario:
    def __init__(self, nome, sobrenome, endereco, email, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.endereco = endereco
        self.email = email
        self.telefone = telefone

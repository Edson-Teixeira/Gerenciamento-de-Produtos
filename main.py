from view import *
from model import *
import os

os.system("cls" if os.name == "nt" else "clear")

# Ao selecionar a sua opção, precione "Enter" para voltar ao Menu inicial.

def menu():
    print("Selecione uma opção: ")
    print("1. Inserir um novo Livro")
    print("2. Inserir um novo Usuario")
    print("3. Realizar um emprestimo")
    print("4. Atualizar data de devolução")
    print("5. Exibir todos os livros emprestados")
    print("6. Exibir todos os livros")
    print("7. Exibir todos os usuarios")
    print("8. Consultar livro")
    print("9. Gerar Relatorio")
    print("0. Sair\n" )

    try:
        escolha = int(input("Digite o número da opção desejada: "))
        return escolha
    except ValueError:
        print("Só aceitamos valores inteiros.")
        g = input()
    

gatilho = True
while gatilho == True: # loop principal do app
    os.system("cls" if os.name == "nt" else "clear")
    escolha = menu()

    if escolha == 1: # Inserimos os dados do novo livro
        os.system("cls" if os.name == "nt" else "clear")
        print("Insira as informção do LIvro")
        titulo = str(input("Digite o Titulo do Livro: "))
        autor = str(input("Digite o Autor do Livro: "))
        editora =str(input("Digite a Editora do Livro: "))
        ano = int(input("Digite o Ano de Publicação: "))
        isbn = str(input("Digite o ISBN do Livro: "))
        livro  = Livro(titulo,autor,editora,ano,isbn)
        inserir_livro(livro)
        g = input()
    
    if escolha == 2: # Inserimos os dados do novo usuario
        os.system("cls" if os.name == "nt" else "clear")
        print("Insira as informações do novo Usuario")
        nome = str(input("Digite o Nome do Novo Usuario: "))
        sobrenome = str(input("Digite o Sobrenome do Nome Usuario: "))
        endereco =str(input("Digite o Endereço do Novo Usuario: "))
        email = str(input("Digite o Email do Novo Usuario: "))
        telefone = str(input("Digite o numero de Telefone do Novo Usuario: "))
        usuario = Usuario(nome,sobrenome,endereco,email,telefone)

        inserir_usuarios(usuario)
        g = input()

    if escolha == 3: # Inserimos os dados do novo emprestimo
        os.system("cls" if os.name == "nt" else "clear")
        print("Insira as informaçoes do emprestimo")
        id_livro = str(input("Digite o ID do Livro: "))
        id_usuario = str(input("Digite o ID do Usuario: "))
        data_emprestimo =str(input("Digite a Data do Emprestimo: "))
        data_devolucao = str(input("Digite a Data da Devolução (Caso não tenha, deixe em banco): "))
        if data_devolucao == "":
            data_devolucao = None

        inserir_emprestimos(id_livro,id_usuario,data_emprestimo,data_devolucao)
        g = input()

    if escolha == 4: # Aqui damos entrada na devolução do livro
        os.system("cls" if os.name == "nt" else "clear")
        data_devolucao = str(input("Digite a Data de Devolução: "))
        id_emprestimo = str(input("Digite o ID do Emprestimo: "))

        atualizar_devolucao(data_devolucao,id_emprestimo)
        print("Data atualizada: Livro devolvido")
        g = input()

    if escolha == 5: # Exibimos todos os livros emprestados
        os.system("cls" if os.name == "nt" else "clear")
        exibir_emprestimos_devolucoes()
        g = input()

    if escolha == 6: # Exibimos todos os livros
        os.system("cls" if os.name == "nt" else "clear")
        exibir_livros()
        g = input()

    if escolha == 7: # Exibimos todos os usuarios
        os.system("cls" if os.name == "nt" else "clear")
        exibir_usuario()
        g = input()

    if escolha == 8: # Consultamos os livros por Nome, Autor ou Ano de publicação
        consulta2 = str(input("Faça sua pesquisa:"))
        os.system("cls" if os.name == "nt" else "clear")
        consultar_livros(consulta2)
        g = input()

    if escolha == 9: # apresenta um relatorio de todos os livros, todos os usuarios e todos os livros emprestados com suas quantidades
        os.system("cls" if os.name == "nt" else "clear")
        gerar_relatorio_pdf()
        # print("Esta Opção esta em desenvolvimento no momento, tente novametente mais tarde (º-º) ")
        g = input()

    if escolha == 0: # Fecha o App
        os.system("cls" if os.name == "nt" else "clear")
        gatilho = False

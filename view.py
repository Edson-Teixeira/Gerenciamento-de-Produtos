import sqlite3
import pandas as pd
from fpdf import FPDF


# conecta ao banco de dados
def conectar():
    con = sqlite3.connect("dados.db")
    return con

# funcao: inserir novo livro
def inserir_livro(livro):
    titulo = livro.titulo
    autor = livro.autor
    editora = livro.editora
    ano_publicado = livro.ano
    isbn = livro.isbn
    quantidade_total = 50
    quantidade_disponivel = 50

    conn = conectar()
    try:
        conn.execute("INSERT INTO livros(titulo, autor, editora, ano_publicado, isbn,quantidade_total,quantidade_disponivel) VALUES(?, ?, ?, ?, ?, ?, ?)",
                     (titulo, autor, editora, ano_publicado, isbn, quantidade_total, quantidade_disponivel))
        conn.commit()  # Confirma a inserção
        print("Livro inserido com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir o livro: {e}")
    finally:
        conn.close()  # Fecha a conexão

# funcao: inserir novo usuarios
def inserir_usuarios(usuario):
    nome = usuario.nome
    sobrenome = usuario.sobrenome
    endereco = usuario.endereco
    email = usuario.email
    telefone = usuario.telefone

    conn = conectar()
    try:
        conn.execute("INSERT INTO usuarios(nome, sobrenome, endereco, email, telefone) VALUES(?, ?, ?, ?, ?)",
                     (nome, sobrenome, endereco, email, telefone))
        conn.commit()  # Confirma a inserção
        print("Usuário inserido com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir o usuário: {e}")
    finally:
        conn.close()  # Fecha a conexão

# funcao: inserir novos Emprestimos / Devolucoes
def inserir_emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao):
    conn = conectar()
    try:
        # Verificar a quantidade disponível do livro
        quantidade_disponivel = conn.execute("SELECT quantidade_disponivel FROM livros WHERE id = ?", (id_livro,)).fetchone()
        
        if quantidade_disponivel and quantidade_disponivel[0] > 0:
            # Inserir o empréstimo
            conn.execute("INSERT INTO emprestimos(id_livros, id_usuarios, data_emprestimo, data_devolucao) VALUES(?, ?, ?, ?)",
                         (id_livro, id_usuario, data_emprestimo, data_devolucao))
            conn.commit()  # Confirma a inserção

            # Atualizar a quantidade disponível
            nova_quantidade = quantidade_disponivel[0] - 1
            conn.execute("UPDATE livros SET quantidade_disponivel = ? WHERE id = ?", (nova_quantidade, id_livro))
            conn.commit()  # Confirma a atualização

            print("Empréstimo inserido com sucesso!")
        else:
            print("Não há cópias disponíveis desse livro.")

    except Exception as e:
        print(f"Ocorreu um erro ao inserir o empréstimo: {e}")
    finally:
        conn.close()

# funcao: exibir todos os Livros
def exibir_livros():
    conn = conectar()
    livros = conn.execute("SELECT * FROM livros").fetchall()
    conn.close()

    if not livros:
        print("Nenhum livro encontrado na Biblioteca.")
    print("Livros na Bibliotenca: \n")
    for livro in livros:
        print(f"ID: {livro[0]}")
        print(f"Titulo: {livro[1]}")
        print(f"Autor: {livro[2]}")
        print(f"Editora: {livro[3]}")
        print(f"Ano de Publicação: {livro[4]}")
        print(f"ISBN: {livro[5]}")
        print(f"Estoque Total: {livro[6]}")
        print(f"Estoque Disponivel: {livro[7]}")
        print("\n")

# funcao: exibir todos os Usuarios
def exibir_usuario():
    conn = conectar()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()

    if not usuarios:
        print("Nenhum Usuario encontrado no Banco.")
    print("Usuarios no Banco: \n")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}")
        print(f"Nome: {usuario[1]}")
        print(f"sobrenome: {usuario[2]}")
        print(f"Endereco: {usuario[3]}")
        print(f"Email: {usuario[4]}")
        print(f"Telefone: {usuario[5]}")
        print("\n")

# funcao: exibir todos os Emprestimos
def exibir_emprestimos_devolucoes():
    conn = conectar()
    emprestimos = conn.execute("SELECT livros.titulo, usuarios.nome, usuarios.sobrenome, emprestimos.id, emprestimos.data_emprestimo, emprestimos.data_devolucao, emprestimos.status\
                                FROM livros\
                                INNER JOIN emprestimos ON livros.id = emprestimos.id_livros\
                                INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuarios\
                                WHERE emprestimos.data_devolucao IS NULL").fetchall()
    conn.close()

    if not emprestimos:
        print("Nenhum empréstimo em aberto encontrado.")
    else:
        for emprestimo in emprestimos:
            print(f"Livro: {emprestimo[0]}")
            print(f"Nome: {emprestimo[1]}")
            print(f"sobrenome: {emprestimo[2]}")
            print(f"ID do Emprestimo: {emprestimo[3]}")
            print(f"Data do Emprestimo: {emprestimo[4]}")
            print(f"Data da Devolução: {emprestimo[5]}")
            print(f"Status do Emprestimo: {emprestimo[6]}")
            print("\n")

# funcao: atualizar as datas de devolução dos emprestimos
def atualizar_devolucao(data_devolucao, id_emprestimo):
    from datetime import datetime
    
    conn = conectar()
    try:
        emprestimo = conn.execute("SELECT data_emprestimo, id_livros FROM emprestimos WHERE id = ?", (id_emprestimo,)).fetchone()

        if emprestimo:
            data_emprestimo, id_livro = emprestimo

            data_emprestimo = datetime.strptime(data_emprestimo, "%d/%m/%Y")
            data_devolucao = datetime.strptime(data_devolucao, "%d/%m/%Y")

            if data_devolucao >= data_emprestimo:
                conn.execute("UPDATE emprestimos SET data_devolucao = ?, status = 'fechado' WHERE id = ?", 
                             (data_devolucao.strftime("%d/%m/%Y"), id_emprestimo))
                conn.commit()

                conn.execute("UPDATE livros SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id = ?", 
                             (id_livro,))
                conn.commit()

                print("Data de devolução atualizada com sucesso e quantidade disponível do livro incrementada!")
            else:
                print("Erro: A data de devolução não pode ser menor que a data de empréstimo.")
        else:
            print("Empréstimo não encontrado.")

    except Exception as e:
        print(f"Ocorreu um erro ao atualizar a devolução: {e}")
    finally:
        conn.close()

# funcao: exibir todas as informaçoes ( )
def listar_informacoes():
    conn = conectar()
    try:
        livros_disponiveis = conn.execute("SELECT titulo FROM livros WHERE quantidade_disponivel > 0").fetchall()
        print("Livros Disponíveis:")
        if livros_disponiveis:
            for livro in livros_disponiveis:
                print(f"- {livro[0]}")
        else:
            print("Nenhum livro disponível.")

        print("\n" + "-"*30 + "\n")

        livros_emprestados = conn.execute("SELECT livros.titulo, usuarios.nome, usuarios.sobrenome FROM emprestimos "
                                           "INNER JOIN livros ON livros.id = emprestimos.id_livros "
                                           "INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuarios "
                                           "WHERE emprestimos.data_devolucao IS NULL").fetchall()
        print("Livros Emprestados:")
        if livros_emprestados:
            for emprestimo in livros_emprestados:
                print(f"- {emprestimo[0]} (Emprestado por: {emprestimo[1]} {emprestimo[2]})")
        else:
            print("Nenhum livro emprestado.")

        print("\n" + "-"*30 + "\n")

        usuarios_cadastrados = conn.execute("SELECT nome, sobrenome FROM usuarios").fetchall()
        print("Usuários Cadastrados:")
        if usuarios_cadastrados:
            for usuario in usuarios_cadastrados:
                print(f"- {usuario[0]} {usuario[1]}")
        else:
            print("Nenhum usuário cadastrado.")

    except Exception as e:
        print(f"Ocorreu um erro ao listar as informações: {e}")
    finally:
        conn.close()

# funcao: exporta um relatorio e faz um print das informaçoes no prompt ( )
def gerar_relatorio_pdf(nome_arquivo="relatorio_biblioteca.pdf"):
    conn = conectar()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório da Biblioteca", ln=True, align="C")
    
    # LIVROS CADASTRADOS
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Livros Cadastrados:", ln=True)
    pdf.set_font("Arial", "", 10)
    livros = conn.execute("SELECT * FROM livros").fetchall()
    if livros:
        print("\nLivros Cadastrados:")
        for livro in livros:
            pdf.multi_cell(0, 10, f"ID: {livro[0]} \nTítulo: {livro[1]} \nAutor: {livro[2]} \nEditora: {livro[3]} \nAno: {livro[4]} \nISBN: {livro[5]} \nTotal: {livro[6]} \nDisponível: {livro[7]} \n_________________")
            print(f"ID: {livro[0]} | Título: {livro[1]} | Total: {livro[6]} | Disponível: {livro[7]}" )
    else:
        pdf.cell(0, 10, "Nenhum livro cadastrado.", ln=True)
        print("Nenhum livro cadastrado.")

    pdf.ln(5)

    # USUÁRIOS CADASTRADOS
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Usuários Cadastrados:", ln=True)
    pdf.set_font("Arial", "", 10)
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    if usuarios:
        print("\nUsuários Cadastrados:")
        for usuario in usuarios:
            pdf.multi_cell(0, 10, f"ID: {usuario[0]} \nNome: {usuario[1]} {usuario[2]} \nEndereço: {usuario[3]} \nEmail: {usuario[4]} \nTelefone: {usuario[5]} \n_________________")
            print(f"ID: {usuario[0]} | Nome: {usuario[1]} {usuario[2]}")
    else:
        pdf.cell(0, 10, "Nenhum usuário cadastrado.", ln=True)
        print("Nenhum usuário cadastrado.")

    pdf.ln(5)

    # EMPRÉSTIMOS EM ABERTO (agrupados por livro)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Empréstimos em Aberto:", ln=True)
    pdf.set_font("Arial", "", 10)
    emprestimos = conn.execute("""
        SELECT livros.id, livros.titulo, COUNT(*) as quantidade
        FROM emprestimos
        INNER JOIN livros ON livros.id = emprestimos.id_livros
        WHERE emprestimos.status = 'aberto'
        GROUP BY livros.id, livros.titulo
    """).fetchall()
    if emprestimos:
        print("\nEmpréstimos em Aberto:")
        for emp in emprestimos:
            pdf.multi_cell(0, 10, f"ID do Livro: {emp[0]} \nTítulo: {emp[1]} \nQuantidade de Empréstimos Abertos: {emp[2]} \n_________________")
            print(f"ID: {emp[0]} | Nome: {emp[1]} — Empréstimos em aberto: {emp[2]}")
            # print(f"Livro: {emp[1]} (ID: {emp[0]}) — Empréstimos em aberto: {emp[2]}")
    else:
        pdf.cell(0, 10, "Nenhum empréstimo em aberto.", ln=True)
        print("Nenhum empréstimo em aberto.")

    conn.close()
    pdf.output(nome_arquivo)
    print(f"\nRelatório gerado com sucesso: {nome_arquivo}")

def consultar_livros(titulo):
    conn = conectar()
    titulo = str(titulo).strip()
    try:
        query = "SELECT * FROM livros WHERE titulo LIKE ?"
        params = [f"%{titulo}%"]
        resultados = conn.execute(query, params).fetchall()

        if not resultados:
            query1 = "SELECT * FROM livros WHERE autor LIKE ?"
            params1 = [f"%{titulo}%"]
            resultados = conn.execute(query1, params1).fetchall()

        if not resultados:
            query2 = "SELECT * FROM livros WHERE ano_publicado = ?"
            params2 = [titulo]
            resultados = conn.execute(query2, params2).fetchall()

        if not resultados:  
            print("Nenhum livro encontrado com os critérios informados.")
        else:
            print("Livros encontrados:\n")
            print(f"Pesquisa: {titulo}\n")
            for livro in resultados:
                print(f"ID: {livro[0]}")
                print(f"Título: {livro[1]}")
                print(f"Autor: {livro[2]}")
                print(f"Editora: {livro[3]}")
                print(f"Ano de Publicação: {livro[4]}")
                print(f"ISBN: {livro[5]}")
                print(f"Estoque Total: {livro[6]}")
                print(f"Estoque Disponível: {livro[7]}")
                print("-" * 30)

    except Exception as e:
        print(f"Ocorreu um erro na consulta: {e}")
    finally:
        conn.close()

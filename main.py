from classes import Autor, Usuario, Livro, Exemplar, Emprestimo, Biblioteca

# Criando Autores
autor1 = Autor("Autor 1", "123456789", "Brasileiro")
autor2 = Autor("Autor 2", "987654321", "Americano")

# Criando Livros
livro1 = Livro("Livro 1", "Editora A", ["Ficção"])
livro2 = Livro("Livro 2", "Editora B", ["Não-Ficção"])

# Criando Exemplares
exemplar1 = Exemplar(livro1)
exemplar2 = Exemplar(livro1)
exemplar3 = Exemplar(livro2)

# Adicionando Exemplares aos Livros
livro1.adicionar_exemplar(exemplar1)
livro1.adicionar_exemplar(exemplar2)
livro2.adicionar_exemplar(exemplar3)

# Criando Usuário
usuario1 = Usuario("Usuário 1", "999999999", "Brasileiro")

# Criando Biblioteca
biblioteca = Biblioteca("Biblioteca Municipal")

# Realizando Empréstimo
emprestimo = biblioteca.realizar_emprestimo(livro1, usuario1)

if emprestimo:
    print("Empréstimo realizado com sucesso!")
    print("Data de Empréstimo:", emprestimo.data_emprestimo)
    print("Data de Devolução:", emprestimo.data_devolucao)
else:
    print("Livro indisponível para empréstimo.")

# Devolvendo Livro
if emprestimo:
    if biblioteca.registrar_devolucao(emprestimo):
        print("Devolução realizada com sucesso!")
    else:
        print("Erro ao devolver o livro.")
from datetime import datetime, timedelta

class Pessoa:
    def __init__(self, nome, telefone, nacionalidade):
        self.nome = nome
        self.telefone = telefone
        self.nacionalidade = nacionalidade

class Autor(Pessoa):
    def __init__(self, nome, telefone, nacionalidade):
        super().__init__(nome, telefone, nacionalidade)

class Usuario(Pessoa):
    def __init__(self, nome, telefone, nacionalidade):
        super().__init__(nome, telefone, nacionalidade)

class Livro:
    def __init__(self, titulo, editora, generos):
        self.titulo = titulo
        self.editora = editora
        self.generos = generos
        self.exemplares_disponiveis = []

    def adicionar_exemplar(self, exemplar):
        self.exemplares_disponiveis.append(exemplar)

    def emprestar_exemplar(self):
        if len(self.exemplares_disponiveis) > 0:
            exemplar_emprestado = self.exemplares_disponiveis.pop()
            return exemplar_emprestado
        else:
            return None

class Exemplar:
    def __init__(self, livro):
        self.livro = livro
        self.emprestado = False
        self.data_emprestimo = None

    def emprestar(self):
        if not self.emprestado:
            self.emprestado = True
            self.data_emprestimo = datetime.now()
            return True
        else:
            return False

    def devolver(self):
        if self.emprestado:
            self.emprestado = False
            self.data_emprestimo = None
            return True
        else:
            return False

class Emprestimo:
    def __init__(self, exemplar, usuario):
        self.exemplar = exemplar
        self.usuario = usuario
        self.data_emprestimo = datetime.now()
        self.data_devolucao = None

    def registrar_devolucao(self):
        if self.exemplar.devolver():
            self.data_devolucao = datetime.now()
            return True
        else:
            return False

class Biblioteca:
    def __init__(self, nome):
        self.nome = nome
        self.livros = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)

    def realizar_emprestimo(self, livro, usuario):
        exemplar = livro.emprestar_exemplar()
        if exemplar:
            emprestimo = Emprestimo(exemplar, usuario)
            return emprestimo
        else:
            return None

    def registrar_devolucao(self, emprestimo):
        return emprestimo.registrar_devolucao()
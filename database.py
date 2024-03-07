import sqlite3
from datetime import datetime, timedelta

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Criação das Tabelas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Autores (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        telefone TEXT,
        nacionalidade TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Editoras (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Livros (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        editora_id INTEGER,
        FOREIGN KEY (editora_id) REFERENCES Editoras(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Exemplares (
        id INTEGER PRIMARY KEY,
        livro_id INTEGER,
        emprestado INTEGER,
        FOREIGN KEY (livro_id) REFERENCES Livros(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        telefone TEXT,
        nacionalidade TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Emprestimos (
        id INTEGER PRIMARY KEY,
        exemplar_id INTEGER,
        usuario_id INTEGER,
        data_emprestimo TEXT,
        data_devolucao TEXT,
        FOREIGN KEY (exemplar_id) REFERENCES Exemplares(id),
        FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
    )
''')

# Criação da tabela AutoresLivros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AutoresLivros (
        autor_id INTEGER,
        livro_id INTEGER,
        FOREIGN KEY (autor_id) REFERENCES Autores(id),
        FOREIGN KEY (livro_id) REFERENCES Livros(id),
        PRIMARY KEY (autor_id, livro_id)
    )
''')

# Inserção de Dados de Exemplo
autores = [
    ("Lygia Fagundes Teles", "123456789", "Brasileira"),
    ("Toni Morrison", "987654321", "Americana")
]

cursor.executemany('INSERT INTO Autores (nome, telefone, nacionalidade) VALUES (?, ?, ?)', autores)

editoras = [
    ("Editora Brasil",),
    ("Editora America",)
]

cursor.executemany('INSERT INTO Editoras (nome) VALUES (?)', editoras)

livros = [
    ("As Meninas", 1),
    ("O Olho Mais Azul", 2)
]

cursor.executemany('INSERT INTO Livros (titulo, editora_id) VALUES (?, ?)', livros)

exemplares = [
    (1, 0),
    (1, 0),
    (2, 0)
]

cursor.executemany('INSERT INTO Exemplares (livro_id, emprestado) VALUES (?, ?)', exemplares)

usuarios = [
    ("Usuária Ana", "999999999", "Brasileira")
]

cursor.executemany('INSERT INTO Usuarios (nome, telefone, nacionalidade) VALUES (?, ?, ?)', usuarios)

# Consultas SQL
def execute_query(query):
    cursor.execute(query)
    return cursor.fetchall()

# Listar todos os livros disponíveis
query = '''
    SELECT Livros.titulo
    FROM Livros
    INNER JOIN Exemplares ON Livros.id = Exemplares.livro_id
    WHERE Exemplares.emprestado = 0
'''
livros_disponiveis = execute_query(query)
print("Livros Disponíveis:")
for livro in livros_disponiveis:
    print(livro[0])

# Encontrar todos os livros emprestados no momento
query = '''
    SELECT Livros.titulo
    FROM Livros
    INNER JOIN Exemplares ON Livros.id = Exemplares.livro_id
    WHERE Exemplares.emprestado = 1
'''
livros_emprestados = execute_query(query)
print("\nLivros Emprestados:")
for livro in livros_emprestados:
    print(livro[0])

# Localizar os livros escritos por um autor específico
autor_especifico = "Toni Morrison"
query = f'''
    SELECT Livros.titulo
    FROM Livros
    INNER JOIN AutoresLivros ON Livros.id = AutoresLivros.livro_id
    INNER JOIN Autores ON AutoresLivros.autor_id = Autores.id
    WHERE Autores.nome = "{autor_especifico}"
'''
livros_autor_especifico = execute_query(query)
print(f"\nLivros escritos por {autor_especifico}:")
for livro in livros_autor_especifico:
    print(livro[0])

# Verificar o número de cópias disponíveis de um determinado livro
livro_especifico = "As Meninas"
query = f'''
    SELECT COUNT(*)
    FROM Exemplares
    INNER JOIN Livros ON Exemplares.livro_id = Livros.id
    WHERE Livros.titulo = "{livro_especifico}" AND Exemplares.emprestado = 0
'''
num_copias_disponiveis = execute_query(query)[0][0]
print(f"\nNúmero de cópias disponíveis de {livro_especifico}: {num_copias_disponiveis}")

# Mostrar os empréstimos em atraso
data_limite_devolucao = datetime.now() - timedelta(days=7)
query = f'''
    SELECT Livros.titulo, Emprestimos.data_devolucao
    FROM Emprestimos
    INNER JOIN Exemplares ON Emprestimos.exemplar_id = Exemplares.id
    INNER JOIN Livros ON Exemplares.livro_id = Livros.id
    WHERE Emprestimos.data_devolucao < "{data_limite_devolucao}"
'''
emprestimos_atrasados = execute_query(query)
print("\nEmpréstimos em Atraso:")
for emprestimo in emprestimos_atrasados:
    print(f"{emprestimo[0]} - Data de Devolução: {emprestimo[1]}")

# Atualizações e Exclusões
autor_id = 1
novo_telefone = "9876543210"
query = f'''
    UPDATE Autores
    SET telefone = "{novo_telefone}"
    WHERE id = {autor_id}
'''
cursor.execute(query)

# Salvar e fechar conexão
conn.commit()
conn.close()
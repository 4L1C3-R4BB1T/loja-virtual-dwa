SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco FLOAT NOT NULL,
        descricao TEXT NOT NULL,
        estoque INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id))
"""

SQL_INSERIR = """
    INSERT INTO produto(nome, preco, descricao, estoque, id_categoria)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT p.id, p.nome, p.preco, p.descricao, p.estoque, p.id_categoria, c.descricao, c.cor
    FROM produto p, categoria c
    WHERE p.id_categoria = c.id
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE produto
    SET nome=?, preco=?, descricao=?, estoque=?, id_categoria=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM produto    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT p.id, p.nome, p.preco, p.descricao, p.estoque, p.id_categoria, c.descricao
    FROM produto p, categoria c
    WHERE p.id=?
    AND p.id_categoria=c.id
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM produto
"""

SQL_OBTER_BUSCA = """
    SELECT p.id, p.nome, p.preco, p.descricao, p.estoque
    FROM 
        produto p INNER JOIN categoria c ON c.id  = p.id_categoria
    WHERE (p.nome LIKE ? OR p.descricao LIKE ?) #2
    ORDER BY #1
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM produto
    WHERE nome LIKE ? OR descricao LIKE ?
"""

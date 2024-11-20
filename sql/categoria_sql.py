SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        descricao TEXT NOT NULL UNIQUE,       
        cor TEXT NOT NULL CHECK (LENGTH(cor) <= 255) 
    );
"""

SQL_INSERIR = """
    INSERT INTO categoria(descricao, cor)
    VALUES (?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, descricao, cor
    FROM categoria
    ORDER BY id
"""

SQL_ALTERAR = """
    UPDATE categoria
    SET descricao=?, cor=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM categoria    
    WHERE id=?
"""

SQL_OBTER_POR_ID = """
    SELECT id, descricao, cor
    FROM categoria
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM categoria
"""

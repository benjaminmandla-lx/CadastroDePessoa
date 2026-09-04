# database.py
import sqlite3

DB_FILE = "cadastro.db"

def criar_tabela():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        documento TEXT NOT NULL,
        email TEXT NOT NULL,
        celular TEXT NOT NULL,
        cep TEXT NOT NULL,
        logradouro TEXT NOT NULL,
        numero TEXT NOT NULL,
        complemento TEXT,
        bairro TEXT NOT NULL,
        cidade TEXT NOT NULL,
        estado TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def salvar_pessoa(dados: dict) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO pessoas (
            nome, tipo, documento, email, celular, cep,
            logradouro, numero, complemento, bairro, cidade, estado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados["nome"], dados["tipo"], dados["documento"], dados["email"],
            dados["celular"], dados["cep"], dados["logradouro"], dados["numero"],
            dados.get("complemento", ""), dados["bairro"], dados["cidade"], dados["estado"]
        ))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
    
def listar_pessoas():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM pessoas ORDER BY id DESC")

    pessoas = cur.fetchall()

    conn.close()

    return pessoas

def pesquisar_pessoas(texto):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM pessoas
        WHERE nome LIKE ?
        ORDER BY nome
    """, (f"%{texto}%",))

    pessoas = cur.fetchall()

    conn.close()

    return pessoas

def excluir_pessoa(id_pessoa):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM pessoas WHERE id = ?",
            (id_pessoa,)
        )

        conn.commit()
        conn.close()

        return True

    except Exception:
        return False
    
def buscar_pessoa(id_pessoa):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM pessoas WHERE id = ?",
        (id_pessoa,)
    )

    pessoa = cur.fetchone()

    conn.close()

    return pessoa

def atualizar_pessoa(id_pessoa, dados):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("""
            UPDATE pessoas SET
                nome = ?,
                tipo = ?,
                documento = ?,
                email = ?,
                celular = ?,
                cep = ?,
                logradouro = ?,
                numero = ?,
                complemento = ?,
                bairro = ?,
                cidade = ?,
                estado = ?
            WHERE id = ?
        """, (
            dados["nome"],
            dados["tipo"],
            dados["documento"],
            dados["email"],
            dados["celular"],
            dados["cep"],
            dados["logradouro"],
            dados["numero"],
            dados["complemento"],
            dados["bairro"],
            dados["cidade"],
            dados["estado"],
            id_pessoa
        ))

        conn.commit()
        conn.close()

        return True

    except Exception:
        return False
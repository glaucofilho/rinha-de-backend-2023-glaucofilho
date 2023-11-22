from sqlalchemy import text

CONSULTA_PESSOA_SQL = text(
    "SELECT id, apelido, nome, nascimento, "
    "stack FROM pessoas p WHERE p.id = :id LIMIT 1"
)

BUSCA_PESSOA_SQL = text(
    "SELECT id, apelido, nome, nascimento, "
    "stack FROM pessoas p WHERE p.busca ILIKE :t LIMIT 50"
)

INSERIR_PESSOA_SQL = "INSERT INTO pessoas (id, apelido, nome, nascimento, stack, busca) VALUES (%(id)s, %(apelido)s, %(nome)s, %(nascimento)s, %(stack)s, %(busca)s) ON conflict (apelido) do update set id = excluded.id, apelido = excluded.apelido, nome = excluded.nome, nascimento = excluded.nascimento, stack = excluded.stack, busca = excluded.busca"


async def insert_into_db(pool, persons):
    async with pool.connection() as conn:
        async with conn.transaction() as t:
            cur = t.connection.cursor()
            await cur.executemany(INSERIR_PESSOA_SQL, persons)

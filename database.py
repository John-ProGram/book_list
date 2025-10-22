from sqlalchemy import text
from sqlalchemy.engine import create_engine

# Cria uma conexão com o banco PostgreSQL usando SQLAlchemy puro.
engine = create_engine(url="postgresql://postgres:1234@127.0.0.1:5432/postgres")

# Define uma classe que executa comandos SQL. Se query=True, retorna os resultados.
class DatabaseManager:
    engine = engine

    def execute_sql_str(self, sql: str, query=False):
        with self.engine.connect() as conn:
            with conn.begin():
                result = conn.execute(text(sql))
                if query:
                    return result.fetchall()
                return None
            
# Ex: print(DatabaseManager().execute_sql_str("SELECT version()", query=True))
DatabaseManager().execute_sql_str("select version()", query=True)
print(DatabaseManager().execute_sql_str("select version()", query=True))

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=True)


server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = quote_plus(os.getenv("SQL_PASSWORD"))


conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"


engine = create_engine(conn_str)

try:

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )
        print("Conexão estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar: {e}")

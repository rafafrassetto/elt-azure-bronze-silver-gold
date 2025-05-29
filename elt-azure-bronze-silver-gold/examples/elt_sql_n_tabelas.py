import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
directory_name = os.getenv("ADLS_DIRECTORY_NAME")
sas_token = os.getenv("ADLS_SAS_TOKEN")


server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
schema = os.getenv("SQL_SCHEMA")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")


password = quote_plus(password)


conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"


engine = create_engine(conn_str)


query = (
    f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{schema}'"
)


file_system_client = DataLakeServiceClient(
    account_url=f"https://{account_name}.dfs.core.windows.net",
    credential=sas_token,
    api_version="2020-02-10",
)


try:
    directory_client = file_system_client.get_file_system_client(
        file_system_name
    ).get_directory_client(directory_name)
    directory_client.create_directory()
except ResourceExistsError:
    print(f"O diretório '{directory_name}' já existe.")


df_tables = pd.read_sql(query, engine)


for index, row in df_tables.iterrows():
    table_name = row["table_name"]
    query = f"SELECT * FROM {schema}.{table_name}"
    df = pd.read_sql(query, conn_str)


    file_client = directory_client.get_file_client(f"{table_name}.csv")
    data = df.to_csv(index=False).encode()
    file_client.upload_data(data, overwrite=True)
    print(f"Dados da tabela '{table_name}' carregados com sucesso.")

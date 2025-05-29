import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv


load_dotenv()


server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
schema = os.getenv("SQL_SCHEMA")
table_name = os.getenv("SQL_TABLE_NAME")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")


account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
directory_name = database
sas_token = os.getenv("ADLS_SAS_TOKEN")



password = quote_plus(password)


query = f"SELECT * FROM {schema}.{table_name}"


conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
df = pd.read_sql(query, conn_str)


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


file_client = directory_client.get_file_client(f"{table_name}.csv")


file_client.create_file()


data = df.to_csv(index=False).encode()


file_client.upload_data(data, overwrite=True)

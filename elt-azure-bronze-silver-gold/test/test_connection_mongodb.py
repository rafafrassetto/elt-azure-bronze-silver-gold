from pymongo import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

mongo_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongo_uri, server_api=ServerApi("1"))

try:

    client.admin.command("ping")
    print("Conexão estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar: {e}")

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoConfig:
    def __init__(self, username, password, collection):
        self.username = username
        self.password = password
        self.collection = collection

    def get_connection_string(self):
        return f"mongodb+srv://{self.username}:{self.password}@{self.collection}.kjvvsvm.mongodb.net/?retryWrites=true&w=majority&appName={self.collection}"  # noqa


username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
collection = os.getenv("MONGO_COLLECTION")

config = MongoConfig(username, password, collection)
connection_string = config.get_connection_string()
client = MongoClient(connection_string)
db = client[config.collection]["futStats"]
collection_players = db["Players"]
collection_stats = db["PlayerStats"]
collection_matches = db["Matches"]

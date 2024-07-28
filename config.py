import os
import json

FOLDER_DATABASE_ID = os.getenv("FOLDER_DATABASE_ID")
API_KEY = os.getenv("API_KEY")
COLLECTION_SETS = json.loads(os.getenv("COLLECTION_SETS"))
DB_PATH = 'db/pokemon_cards.db'

# pip install databases[postgresql]
from databases import Database

from config import DB_URL

db = Database(DB_URL)

import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get('api_id')
API_HASH = os.environ.get('api_hash')
PHONE = os.environ.get('phone')
PASSWORD = os.environ.get('password')
CHAT_ID = int(os.environ.get('chat_id'))
MY_CHAT_ID = int(os.environ.get('my_chat_id'))
BOT_TOKEN = os.environ.get('bot_token')
DB_URL = os.environ.get('db_url')
CAPTIONS = [None] if True else ['ахаха', ':)', 'лол', None]

import os

from dotenv import load_dotenv

load_dotenv()


class MyArguments:
    api_id = os.environ.get('api_id')
    api_hash = os.environ.get('api_hash')
    phone = os.environ.get('phone')
    password = os.environ.get('password')
    chat_id = int(os.environ.get('chat_id'))
    file_path = os.environ.get('file_path')


args = MyArguments()
CAPTIONS = [
    'ахаха',
    ':)',
    'лол',
    None
]

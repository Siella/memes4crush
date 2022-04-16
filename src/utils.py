import re
from datetime import timedelta

from asyncpg.exceptions import (ConnectionDoesNotExistError,
                                ConnectionFailureError)

from src.db import db

time_pattern = re.compile(
    r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?'
)


async def parse_time(time_: str):
    parts = time_pattern.match(time_)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


class EmptyMemePoolError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


def db_connection(f):
    async def wrapper(*args, **kwargs):
        try:
            await db.connect()
        except (ConnectionDoesNotExistError, ConnectionFailureError):
            raise DatabaseConnectionError('Can not connect.')
        else:
            result = await f(*args, **kwargs)
        finally:
            await db.disconnect()
        return result
    return wrapper


@db_connection
async def get_meme():
    try:
        record = await db.fetch_one(
            "SELECT * from meme_pool ORDER BY id"
        )  # FIFO
        meme = record.get('bytes')
    except (ValueError, AttributeError):
        raise EmptyMemePoolError("Memes run out!")
    else:
        await db.execute("DELETE FROM meme_pool "
                         "WHERE id=:id",
                         values={'id': record.get('id')})
        return meme

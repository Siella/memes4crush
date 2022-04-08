import re
from datetime import timedelta
from pathlib import Path

import aiofiles

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


async def get_meme(from_path: str):
    p = Path(from_path)
    meme_files = {
        x: (p / x).stat().st_mtime for x in p.glob('*.*')
        if x.is_file()
    }
    try:
        meme = min(meme_files, key=meme_files.get)  # FIFO
    except ValueError:
        raise EmptyMemePoolError("Memes run out!")
    async with aiofiles.open(meme, 'rb') as file:
        file_bytes = await file.read()
    meme.unlink()  # remove from queue
    return file_bytes

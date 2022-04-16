"""
Bot which sends ur memes to the user.
"""
import asyncio
import logging
import random as rd
import sys
from datetime import datetime

from telethon import TelegramClient

from src.config import API_HASH, API_ID, CAPTIONS, CHAT_ID, PASSWORD, PHONE
from src.utils import (DatabaseConnectionError, EmptyMemePoolError, get_meme,
                       parse_time)

sys.tracebacklimit = 0
logging.basicConfig(level=logging.INFO)


async def main(every: str = '24hr'):
    client = TelegramClient('sender', API_ID, API_HASH)
    await client.start(PHONE, PASSWORD)

    while True:
        try:
            meme = await get_meme()
        except (EmptyMemePoolError, DatabaseConnectionError) as err:
            logging.exception("Failed to get a pic: " + str(err))
        else:
            await client.send_file(
                CHAT_ID, meme, caption=rd.choice(CAPTIONS),
                silent=datetime.now().time().hour in range(0, 8)
            )

        period = await parse_time(every)
        rand_time = await parse_time(''.join([str(rd.randint(0, 900)), 's']))
        rand_sign = rd.choice([1, -1])
        dt = datetime.now() + period + rand_sign * rand_time

        logging.info(
            f"Next meme will be sent {dt.strftime('%d/%m/%Y, %H:%M:%S')}"
        )

        while datetime.now() < dt:
            await asyncio.sleep(1)

asyncio.run(main())

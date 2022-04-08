import asyncio
import logging
import random as rd
import sys
from datetime import datetime

from telethon import TelegramClient

from config import CAPTIONS, args
from utils import EmptyMemePoolError, get_meme, parse_time

sys.tracebacklimit = 0
logging.basicConfig(level=logging.INFO)


async def main(every: str = '24hr'):
    client = TelegramClient('test', args.api_id, args.api_hash)
    await client.start(args.phone, args.password)

    while True:
        try:
            meme = await get_meme(args.file_path)
        except EmptyMemePoolError as err:
            logging.exception("Failed to get a pic: " + str(err))
        else:
            await client.send_file(
                args.chat_id, meme, caption=rd.choice(CAPTIONS),
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

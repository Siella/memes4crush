"""
Bot which saves ur memes into database.
"""
import asyncio
import logging
import sys

from telebot.async_telebot import AsyncTeleBot

from src.config import BOT_TOKEN, MY_CHAT_ID
from src.db import db
from src.utils import db_connection

sys.tracebacklimit = 0
logging.basicConfig(level=logging.INFO)

bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text', 'photo'])
async def meme_handler(message):
    chat_id = message.chat.id
    await asyncio.sleep(1)
    if chat_id != MY_CHAT_ID:
        await bot.send_message(chat_id, "I'm not 4 you!")
    elif not message.photo:
        await bot.send_message(chat_id, "Feed me memes!")
    else:
        @db_connection
        async def save_meme():
            file_path = await bot.get_file(message.photo[-1].file_id)
            downloaded_file = await bot.download_file(file_path.file_path)
            await db.execute(
                "INSERT INTO meme_pool(bytes) "
                "VALUES (:meme_bytes)",
                values={'meme_bytes': downloaded_file}
            )
            await bot.send_message(chat_id, "Om-nom!")
        await save_meme()


asyncio.run(bot.infinity_polling())

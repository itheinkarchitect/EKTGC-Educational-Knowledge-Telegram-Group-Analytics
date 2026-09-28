import asyncio

from telegram_client import client
from messages import get_teacher_messages, get_readers
from excel import save_readings


async def main():
    messages = await get_teacher_messages(limit=10)

    for message in messages:
        readers = await get_readers(message.id)
        save_readings(message, readers)


async def run():
    while True:
        await main()
        print("Excel обновлён.")
        await asyncio.sleep(3600)


with client:
    client.loop.run_until_complete(run())
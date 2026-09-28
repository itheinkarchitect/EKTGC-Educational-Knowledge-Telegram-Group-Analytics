from telethon import functions

from config import GROUP_ID, TEACHER_ID
from telegram_client import client


async def get_readers(message_id):
    result = await client(functions.messages.GetMessageReadParticipantsRequest(
        peer=GROUP_ID,
        msg_id=message_id
    ))

    users = await client.get_participants(GROUP_ID)

    users_dict = {}

    for user in users:
        users_dict[user.id] = user

    readers = []

    for participant in result:
        user = users_dict.get(participant.user_id)

        readers.append({
            "user_id": participant.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "read_at": participant.date
        })

    return readers


async def get_teacher_messages(limit=50):
    messages = await client.get_messages(GROUP_ID, limit=limit)

    teacher_messages = []

    for message in messages:
        if message.sender_id == TEACHER_ID:
            teacher_messages.append(message)

    return teacher_messages
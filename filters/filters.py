from aiogram.types import Message

from db.create_connection import create_connection
from services.services import registration_user


def help_filter(message: Message) -> bool:
    return message.text == '/help'


def is_not_banned_filter(message: Message) -> bool:
    user_id = message.from_user.id
    connection = create_connection()
    if connection:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user is None:
                registration_user(user_id, connection, cursor)
                return True
            return not user[3]


def filter_for_searching_books(message: Message):
    return len(message.text.split()) > 1 and message.text.split()[0] == '/search'
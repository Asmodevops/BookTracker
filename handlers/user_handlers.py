import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from db.create_connection import create_connection
from filters.filters import help_filter, is_not_banned_filter, filter_for_searching_books
from keyboards.inline_kb import button_to_go_to_administration, create_a_keyboard_from_a_list_of_books
from lexicon.lexicon import LEXICON
from services.services import get_a_list_of_books

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart(), is_not_banned_filter)
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON['/start']
    )


@router.message(lambda message: not is_not_banned_filter(message))
async def process_reply_to_blocked_user(message: Message):
    await message.answer(
        text=LEXICON['message_from_banned_user'],
        reply_markup=button_to_go_to_administration()
    )


@router.message(help_filter, is_not_banned_filter)
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON['/help'],
        reply_markup=button_to_go_to_administration()
    )


@router.message(filter_for_searching_books, is_not_banned_filter)
async def process_find_book(message: Message):
    book_name = '+'.join(message.text.replace('/search', '').split())
    books = get_a_list_of_books(book_name)
    if books:
        await message.answer(
            text=f'🔍 Список книг по запросу: <b>{message.text.replace("/search", "")}</b>',
            reply_markup=create_a_keyboard_from_a_list_of_books(books)
        )
    else:
        await message.answer(
            text=f'😥 Я не нашел книг по запросу: <b>{message.text.replace("/search", "")}</b>'
        )

import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from db.create_connection import create_connection
from filters.filters import help_filter, is_not_banned_filter, filter_for_searching_books
from keyboards.inline_kb import button_to_go_to_administration, create_a_keyboard_from_a_list_of_books, \
    create_a_keyboard_for_downloading_books
from lexicon.lexicon import LEXICON
from services.services import get_a_list_of_books, get_information_about_the_book, download_book, delete_book

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
            text=f'{LEXICON["found_books"]} <b>{message.text.replace("/search", "")}</b>',
            reply_markup=create_a_keyboard_from_a_list_of_books(books)
        )
    else:
        await message.answer(
            text=f'{LEXICON["dont_find_the_book"]} <b>{message.text.replace("/search", "")}</b>'
        )


@router.callback_query(is_not_banned_filter, F.data.split(':-:')[0] == 'get_book')
async def process_show_book_information(callback: CallbackQuery):
    book_info = get_information_about_the_book(callback.data.replace('get_book:-:', ''))
    await callback.message.answer(
        text=f'<b>{book_info["title"]}</b>\n\n'
             f'<b>Описание:</b>\n{book_info["anotation"]}',
        reply_markup=create_a_keyboard_for_downloading_books(book_info["download_urls"])
    )
    await callback.answer()


@router.callback_query(is_not_banned_filter, F.data.split(':-:')[0] == 'download_book')
async def process_download_and_send_book(callback: CallbackQuery):
    url = callback.data.replace('download_book:-:', '')
    file_name = download_book(url)
    document = FSInputFile(path=f'downloads/{file_name}')
    await callback.message.answer_document(
        document=document
    )
    delete_book(file_name)
    await callback.answer()
















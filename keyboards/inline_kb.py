from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def button_to_go_to_administration():
    kb_builder = InlineKeyboardBuilder()
    administration_button: InlineKeyboardButton = InlineKeyboardButton(
        text=f'👑 Администрация',
        url=f'{LEXICON["admin_url"]}'
    )
    kb_builder.row(administration_button)
    return kb_builder.as_markup()


def create_a_keyboard_from_a_list_of_books(books):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in books:
        buttons.append(InlineKeyboardButton(
            text=button['book_name'],
            callback_data=f'get_book:-:{button["book_url"]}'
        ))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


def create_a_keyboard_for_downloading_books(urls):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in urls:
        buttons.append(InlineKeyboardButton(
            text=button['extension'],
            callback_data=f'download_book:-:{button["dwnld_url"]}'
        ))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()
import os
import shutil

import requests
import wget
from bs4 import BeautifulSoup
import re


def registration_user(user_id, connection, cursor):
    cursor.execute("INSERT INTO users (user_id, start_date) VALUES (%s, NOW())",
                   (user_id,))
    connection.commit()


def get_a_list_of_books(book_name):
    url = f'https://flibusta.is/booksearch?ask={book_name}&chb=on'
    books: list[dict[str:str]] = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_block = soup.find('div', id='main-wrapper')
    get_books = main_block.find_all('li')
    if get_books is None:
        return books

    for book in get_books:
        if len(books) == 8:
            break
        link = book.find('a', href=re.compile(r'/a/|/b/'))
        if link is not None:
            link = link.get('href')
            d_book = {
                'book_name': book.text,
                'book_url': f'https://flibusta.is{link}'
            }
            books.append(d_book)
    return books


def get_information_about_the_book(url):
    self_book = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_block = soup.find('div', id='main-wrapper')
    book_title = main_block.find('h1', class_='title').text
    anotation = main_block.find_all('p')[1].text if main_block.find_all('p')[1].text != '' else 'Отсутствует'
    dwnlds = []
    download_urls = main_block.find_all('a', href=re.compile(r'/download|/fb2|/epub|/mobi|/pdf'))
    for url in download_urls:
        link = url.get('href')
        d_book = {
            'extension': url.text[1:-1],
            'dwnld_url': f'https://flibusta.is{link}'
        }
        dwnlds.append(d_book)
    self_book['title'] = book_title
    self_book['anotation'] = anotation
    self_book['download_urls'] = dwnlds
    return self_book


def download_book(url):
    save_dir = os.path.join('.', 'downloads')
    if os.path.exists(save_dir) and os.path.isdir(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir)
    wget.download(url, out=save_path)
    file_name = os.listdir(save_dir)[0]
    return file_name


def delete_book(file_name):
    file_path = f'./downloads/{file_name}'
    os.remove(file_path)


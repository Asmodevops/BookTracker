import requests
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
        link = book.find('a', href=re.compile(r'/a/|/b/'))
        if link is not None:
            link = link.get('href')
            d_book = {
                'book_name': book.text,
                'book_url': f'https://flibusta.is{link}'
            }
            books.append(d_book)
    return books[:8]

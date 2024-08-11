def init_db(connection):
    if connection:
        with connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL UNIQUE,
                    start_date TIMESTAMP NOT NULL,
                    is_banned BOOL DEFAULT FALSE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_books (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    book_name TEXT NOT NULL,
                    book_link TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')

            connection.commit()
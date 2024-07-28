import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            username TEXT NOT NULL,
            firstname TEXT NOT NULL,
            adress TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def add_user(self, phone_number, username, firstname, adress):
        self.cursor.execute('''
        INSERT INTO users (phone_number, username, firstname, adress) VALUES (?, ?, ?, ?)
        ''', (phone_number, username, firstname, adress))
        self.connection.commit()

    def get_user_by_username(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
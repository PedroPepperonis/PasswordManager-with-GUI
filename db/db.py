import psycopg2
from psycopg2.extras import DictCursor

class Database():
    def __init__(self, dbname, host, port, user, password):
        self.connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=password)
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def add_password(self, name, url, login, password):
        with self.connection:
            return self.cursor.execute('INSERT INTO Password(name, url, login, password) VALUES(%s, %s, %s, %s)', (name, url, login, password, ))

    def update_password(self, name, password):
        with self.connection:
            return self.cursor.execute('UPDATE Password SET password = %s WHERE name = %s', (password, name, ))

    def get_password(self, name):
        with self.connection:
            self.cursor.execute('SELECT login, password FROM Password WHERE name = %s', (name, ))
            result = self.cursor.fetchall()
            return result

    def get_all(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM password')
            return self.cursor.fetchall()
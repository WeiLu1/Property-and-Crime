import psycopg2
from queries import create_crimes_table
import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


class PostgresDriver(object):

    def __init__(self):
        try:
            self.conn = psycopg2.connect(database=database, user=user, host=host, port=port)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('NO CONNECTION')
            raise e

    def execute_query(self, query):
        self.cursor.execute(query)

    def disconnect(self):
        self.conn.close()
        self.cursor.close()

    def setup(self):
        self.execute_query(create_crimes_table)
        self.conn.commit()
        self.disconnect()


if __name__ == '__main__':
    db = PostgresDriver()
    db.setup()


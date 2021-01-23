import psycopg2
import psycopg2.extras
from queries import create_crimes_table, insert_crime, create_crimes_index
import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


class Postgres(object):

    def __init__(self):
        try:
            self.conn = psycopg2.connect(database=database, user=user, host=host, port=port)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('NO CONNECTION')
            raise e

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def batch_insert(self, batch):
        psycopg2.extras.execute_batch(self.cursor, insert_crime, batch)
        self.conn.commit()

    def disconnect(self):
        self.conn.close()
        self.cursor.close()

    def setup_initial(self):
        """
        Only needs to be done once.
        :return: Table created in Postgres instance on server
        """
        self.execute_query(create_crimes_table)
        self.execute_query(create_crimes_index)
        self.conn.commit()
        self.disconnect()


if __name__ == '__main__':
    db = Postgres()
    db.setup_initial()


import psycopg2
from queries import create_crimes_table


class PostgresDriver(object):

    def __init__(self):
        try:
            self.conn = psycopg2.connect(database="propertycrime", user="postgres", host="127.0.0.1", port="5432")
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


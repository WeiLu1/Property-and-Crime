import psycopg2


def make_connection():
    conn = psycopg2.connect(database='propertycrime', user='postgres', host='127.0.0.1', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM crimes ''')
    result = cursor.fetchone()
    print(result)
    conn.close()


if __name__ == "__main__":
    make_connection()


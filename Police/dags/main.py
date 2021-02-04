from police import PoliceAPI
from utils import load_json
from postgresdriver import Postgres
from datetime import datetime


def insert_crimes_to_db():
    police = PoliceAPI()
    districts = load_json('boroughs_info.json')
    db = Postgres()

    for district in districts:
        borough = district['borough']
        polygon = district['polygon']
        crimes = police.get_crimes_custom_area(polygon)
        if crimes:
            database_insert = []
            for crime in crimes:
                crime_insert = {'id': crime['id'], 'date': crime['month'] + '-01', 'category': crime['category'], 'borough': borough}
                database_insert.append(crime_insert)
            db.batch_insert(database_insert)
            print("batch inserted at: ", datetime.now())
        else:
            print("no new data has come in")
    db.disconnect()


if __name__ == "__main__":
    insert_crimes_to_db()

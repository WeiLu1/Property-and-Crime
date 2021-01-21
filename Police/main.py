import pandas as pd
from police import PoliceAPI
from utils import load_json


def get_crimes():
    police = PoliceAPI()
    districts = load_json('boroughs_info.json')
    all_crimes = []

    for district in districts:
        borough = district['borough']
        polygon = district['polygon']
        crimes = police.get_crimes_custom_area(polygon)
        if crimes:
            for crime in crimes:
                crime['borough'] = borough
            all_crimes.append(crimes)
    return all_crimes


# def data_to_df(data_list):
#     flat_list_crimes = [dictionary for listarr in data_list for dictionary in listarr]
#     df = pd.DataFrame(flat_list_crimes)
#     return df
#
#
# def clean_df(df):
#     df = df.drop(['location', 'context', 'outcome_status', 'persistent_id', 'location_subtype'], axis=1)
#     df = df[['id', 'month', 'borough', 'category', 'location_type']]
#     return df


if __name__ == "__main__":
    get_crimes()

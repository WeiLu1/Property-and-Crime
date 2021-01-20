import pandas as pd
from police import PoliceAPI


city_latlong = {

    'Croydon': ('51.376165', '-0.098234'),
    'Manchester': ('53.480759', '-2.242631'),
    'Brighton': ('50.822530', '-0.137163'),
    'Birmingham': ('52.486243', '-1.890401'),
    'Bristol': ('51.454513', '-2.587910'),
    'Exeter': ('50.718412', '-3.533899'),
    'Norwich': ('52.630886', '1.297355'),
    'Newcastle upon Tyne': ('54.978252', '-1.617780'),
    'Hull': ('53.745671', '-0.336741'),
    'Leeds': ('53.800755', '-1.549077')

           }


def get_crime_data():
    police = PoliceAPI()
    data_all = []
    for city in city_latlong:
        latitude = city_latlong[city][0]
        longitude = city_latlong[city][1]
        data = police.get_crime_at_location(latitude, longitude)
        if data:
            for element in data:
                element['city'] = city
                element['date'] = police.current_month + '-01'
            data_all.append(data)
    return data_all


def data_to_df(data_list):
    flat_list_crimes = [dictionary for listarr in data_list for dictionary in listarr]
    df = pd.DataFrame(flat_list_crimes)
    return df


def clean_df(df):
    df = df.drop(['location', 'context', 'outcome_status', 'persistent_id', 'location_subtype', 'month'], axis=1)
    df = df[['id', 'date', 'city', 'category', 'location_type']]
    return df


if __name__ == "__main__":

    police = PoliceAPI()
    police_force = 'metropolitan'
    metropolitan_codes = police.get_neighbourhood_codes(police_force)
    for pair in metropolitan_codes:
        id = pair['id']
        name = pair['name']
        print(id, name)
        # boundaries = police.get_neighbourhood_boundaries(police_force, id)
        # print(boundaries[0])
        # print()



    # crimes = get_crime_data()
    # crimes_df = data_to_df(crimes)
    # clean = clean_df(crimes_df)
    # clean.to_csv("crimes_july.csv", index=False)



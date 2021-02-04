from datetime import datetime
from utils import (
    get_response,
    write_to_json,
    load_json,
    load_json_local,
    get_linear_spaced_indexes,
    get_last_month
)
from postcode import get_borough


class PoliceAPI(object):

    def __init__(self):
        self.base_url = 'https://data.police.uk/api/'
        self.today = datetime.today()
        self.current_month = str(datetime(self.today.year, self.today.month, 1))[:7]
        self.last_month = get_last_month()
        self.police_force = 'metropolitan'

    def get_crimes_custom_area(self, polygon):
        url = self.base_url + 'crimes-street/all-crime?poly=' + polygon + '&date=' + self.last_month
        response = get_response(url)
        return response

    def get_neighbourhood_codes(self):
        url = self.base_url + self.police_force + '/neighbourhoods'
        response = get_response(url)
        return response

    def get_neighbourhood_boundaries(self, neighbourhood_code):
        url = self.base_url + self.police_force + '/' + neighbourhood_code + '/boundary'
        response = get_response(url)
        return response


def match_police_code_borough(police_obj):
    borough = ''
    borough_total = []

    metropolitan_codes = police_obj.get_neighbourhood_codes()
    for pair in metropolitan_codes:
        boundaries = police_obj.get_neighbourhood_boundaries(pair['id'])

        i = 0
        while i < len(boundaries) - 1:
            lat = boundaries[i]['latitude']
            long = boundaries[i]['longitude']
            borough = get_borough(lat, long)
            if borough == "CAN'T FIND BOROUGH":
                i += 1
            else:
                break

        borough_total.append({'id': pair['id'], 'name': pair['name'], 'borough': borough})
        print(pair['id'] + ', ' + pair['name'] + ', ' + borough)
    write_to_json('borough.json', borough_total)


def get_polygon_police_code(police_obj):
    borough_total = []

    data = load_json_local('borough.json')
    for area in data:
        poly_string = ''
        boundaries = police_obj.get_neighbourhood_boundaries(area['id'])
        indexes = get_linear_spaced_indexes(length=len(boundaries), spacing=100)
        for index in indexes:
            poly_string += str(boundaries[index]['latitude']) + ',' + str(boundaries[index]['longitude']) + ':'
        print(poly_string[:-1])
        borough_total.append({'id': area['id'], 'name': area['name'], 'borough': area['borough'], 'polygon': poly_string[:-1]})
    write_to_json('boroughs_info.json', borough_total)


def get_code_info_to_file():
    """
    Only needs to be done once.
    """
    police = PoliceAPI()
    match_police_code_borough(police)
    get_polygon_police_code(police)


if __name__ == "__main__":
    get_code_info_to_file()

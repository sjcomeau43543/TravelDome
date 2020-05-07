'''
Author:        Gordon
Last modified: 
Status:        In progress


TODO: only return one instance of each activity (dunks listed 5x for ex)
TODO: image location? don't download just link the image
'''

import requests
import json
import time
from math import sin, cos, sqrt, atan2, radians

from activity import Activity



class GooglePlaces(object):
	def __init__(self, apiKey):
		super(GooglePlaces, self).__init__()
		self.apiKey = apiKey

	def search_places_by_coordinate(self, location, radius, types):
		endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
		places = []
		params = {
			'location': location,
			'radius': radius,
			'types': types,
			'key': self.apiKey
		}
		res = requests.get(endpoint_url, params=params)
		results = json.loads(res.content)
		places.extend(results['results'])
		time.sleep(2)
		while "next_page_token" in results:
			params['pagetoken'] = results['next_page_token'],
			res = requests.get(endpoint_url, params=params)
			results = json.loads(res.content)
			places.extend(results['results'])
			time.sleep(2)
		return places

	def get_place_details(self, place_id, fields):
		endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
		params = {
			'placeid': place_id,
			'fields': ",".join(fields),
			'key': self.apiKey
		}
		res = requests.get(endpoint_url, params=params)
		place_details = json.loads(res.content)
		return place_details


def distance_from_coords(coord1, coord2):
	# approximate radius of earth in meter
	R = 6373000
	lat1, lon1 = coord1
	lat2, lon2 = coord2
	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance



def scrape(api, city, state):
	coordinates_list = {'BostonMA':[(42.329126, -71.146042), (42.383613, -71.049872)],
	                    'ProvidenceRI':[(42.329126, -71.146042), (42.383613, -71.049872)],
	                    'NYCNY':[(40.702205, -74.020354), (40.869296, -73.867182)],
	                    'DenverCO':[(39.619346, -105.098746), (39.904585, -104.613042)],
	                    'TampaFL':[(27.845080, -82.552184), (28.170400, -82.264112)],
	                    'HoustonTX':[(29.596677, -95.655682), (29.969183, -95.133634)]
	                    }

	# Smaller area
	# coordinates_list = {'BostonMA':[(42.329126, -71.146042), (42.34, -71.1)],
	#                     'ProvidenceRI':[(42.329126, -71.146042), (42.34, -71.1)],
	#                     'NYCNY':[(40.702205, -74.020354), (40.73, -73.98)],
	#                     'DenverCO':[(39.619346, -105.048746), (39.64, -104.99)],
	#                     'TampaFL':[(27.96, -82.552184), (28.0, -82.50)],
	#                     'HoustonTX':[(29.696677, -95.3), (29.73, -95.25)]
	#                     }
	grid = 0.005
	type_list = ['restaurant', 'bakery', 'cafe', 'amusement_park', 'aquarium', 'art_gallery',
	             'casino', 'library', 'museum', 'night_club', 'park', 'stadium', 'zoo']
	fields = ['name', 'formatted_address', 'rating', 'review']

	city_state = city+state
	activities = []
	place_id_set = set()
	sw_coord, ne_coord = coordinates_list[city_state]
	lat_now, lon_now = sw_coord
	lat_end, lon_end = ne_coord
	distance_grid = distance_from_coords(sw_coord, (lat_now+grid, lon_now))
	rad = distance_grid*1.414/2

	while lat_now < lat_end:
		while lon_now < lon_end:
			print('coordinates:', lat_now, lon_now)
			coord_query = ','.join([str(lat_now), str(lon_now)])

			for type in type_list:
				places = api.search_places_by_coordinate(coord_query, rad, type)
				for place in places:
					place_id = place['place_id']
					if place_id in place_id_set:
						continue
					else:
						place_id_set.add(place_id)
						details = api.get_place_details(place_id, fields)

						place = {}
						rating_sum = 0

						try:
							place['name'] = details['result']['name']
						except KeyError:
							place['name'] = ""

						try:
							place['address'] = details['result']['formatted_address']
						except KeyError:
							place['address'] = ""

						place['avg_visitor_review'] = ''
						place['avg_time_spent'] = ''
						place['photo_location'] = ''
						place['tags'] = []
						place['source'] = 'GoogleMaps'
						place['reviews'] = []

						try:
							reviews = details['result']['reviews']
						except KeyError:
							reviews = []
						print("===================PLACE===================")
						print("Name:", place['name'])
						print("Address:", place['address'])
						# print("==================REVIEWS==================")
						for review in reviews:
							rating_sum += review['rating']
							place['reviews'].append(review['text'])
						if len(reviews) > 0:
							place['avg_visitor_review'] = rating_sum / len(reviews)
							rating_sum = 0

						a = Activity(place['name'], place['address'], place["avg_visitor_review"], None,
						             None, 'GoogleMaps', reviews=place['reviews'], tags=[], get_tags=True)
						activities.append(a)

			lon_now += grid
		lat_now += grid

	return activities

	# file_name = './data/' + city + '.json'
	# with open(file_name, 'w', encoding='utf-8') as f:
	# 	json.dump(activities, f, ensure_ascii=False, indent=1)





if __name__ == "__main__":
	import sys
	# main(sys.argv)
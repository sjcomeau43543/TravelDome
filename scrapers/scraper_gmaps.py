import os, time
import requests, json
import uuid

from activity import Activity



class GooglePlaces(object):
	def __init__(self, apiKey):
		super(GooglePlaces, self).__init__()
		self.apiKey = apiKey


	def text_search(self, query):
		endpoint_url_ts = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
		places = []
		params = {
					# 'location': location,
					# 'radius': radius,
					'key': self.apiKey
				}
		response = requests.get(endpoint_url_ts + 'query=' + query, params=params)
		results = json.loads(response.content)
		places.extend(results['results'])
		time.sleep(2)
		while "next_page_token" in results:
			params['pagetoken'] = results['next_page_token'],
			res = requests.get(endpoint_url_ts + 'query=' + query, params=params)
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


	def get_photo(self, photo_id, photo_reference, maxwidth):
		photo_path_str = '../data/GoogleMaps/photos/' + photo_id + '.png'
		endpoint_url_get_photo = "https://maps.googleapis.com/maps/api/place/photo?"
		photo = []
		params = {
			'photoreference': photo_reference,
			'maxwidth': maxwidth,
			'key': self.apiKey
		}
		response = requests.get(endpoint_url_get_photo, params=params)

		if response.status_code == 200:
			with open(photo_path_str, 'wb') as f:
				f.write(response.content)
		return photo_path_str


def scrape(api, city, state):
	fields = ['name', 'formatted_address', 'rating', 'review', 'url', 'photo']
	queries = []
	queries.append('things to do in ' + city + ', ' + state)
	queries.append('best restaurants in ' + city + ', ' + state)

	places = []
	for query in queries:
		places_found = api.text_search(query)
		places.extend(places_found)

	activities = []
	place_id_set = set()

	for place in places:
		place_id = place['place_id']
		if place_id in place_id_set:
			continue
		else:
			place_id_set.add(place_id)
			details = api.get_place_details(place_id, fields)

			place = {}

			try:
				place['name'] = details['result']['name']
			except KeyError:
				place['name'] = ""

			try:
				place['address'] = details['result']['formatted_address']
			except KeyError:
				place['address'] = ""

			try:
				place['url'] = details['result']['url']
			except KeyError:
				place['url'] = ""

			try:
				place['photo_location'] = details['result']['photos']
			except KeyError:
				place['photo_location'] = []

			try:
				place['avg_visitor_review'] = details['result']['rating']
			except KeyError:
				place['avg_visitor_review'] = ""

			place['avg_time_spent'] = ''
			place['tags'] = []
			place['reviews'] = []

			try:
				reviews = details['result']['reviews']
			except KeyError:
				reviews = []
			print("===================PLACE===================")
			print("Name:", place['name'])
			print("Address:", place['address'])
			for review in reviews:
				place['reviews'].append(review['text'])


			a = Activity(place['name'], place['address'], place["avg_visitor_review"], None,
			             place['photo_location'], 'GoogleMaps', link=place['url'], reviews=place['reviews'], tags=[], get_tags=True)
			activities.append(a)
	return activities


def update_photos_from_reference():
	api = GooglePlaces(apiKey='AIzaSyAoaZRyH4QLOZ4NB88-j4NF-erUJ9VsjhM')
	for file in os.scandir('../data/GoogleMaps/'):
		if file.path.endswith(".json"):
			with open(file, "r") as json_file:
				places = json.load(json_file)

			for place in places:
				if len(place['photo_location']) > 0:
					photo_reference = place['photo_location'][0]['photo_reference']
					photo_id = str(uuid.uuid1())
					photo_path_str = api.get_photo(photo_id, photo_reference, 800)
					place['photo_location'] = photo_path_str
				else:
					place['photo_location'] = ''

			with open(file, "w") as jsonFile:
				json.dump(places, jsonFile, indent=1)

		else:
			continue


if __name__ == "__main__":
	# city = 'Boston'
	# state = 'MA'
	# api = GooglePlaces(apiKey='AIzaSyAoaZRyH4QLOZ4NB88-j4NF-erUJ9VsjhM')
	# activities = scrape(api, city, state)
	#
	# with open("./data/GoogleMaps/" + city + state + ".json", "w") as outfile:
	# 	outfile.write("[\n")
	# 	for activity in activities:
	# 		json.dump(activity.encode(), outfile, indent=1)
	# 		if activity != activities[-1]:
	# 			outfile.write(",")
	# 	outfile.write("]\n")
	update_photos_from_reference()
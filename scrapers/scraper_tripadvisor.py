'''
@author Eda Zhou
@email  ezhou@wpi.edu
'''
import os, json, requests, re
import bs4 as BeautifulSoup

from activity import Activity

def save_json(filename, data):
    i = 0
    while os.path.exists('../data/TripAdvisor/{0}{1}.json'.format(filename, i)): # increment file name
        i += 1
    with open('../data/TripAdvisor/{0}{1}.json'.format(filename, i),
              'a+', encoding='utf-8') as f:
        f.write("[\n")
        for activity in data:
            json.dump(activity.encode(), f, indent=1)
        f.write("]\n")

# takes url, finds <script type="application/ld+json"> and returns contents the soup and json
def url_to_json(url):
    response = requests.get(url)

    if not response.ok:
        print("Oops, something went wrong with GET and/or url: ", url)
        return None

    soup = BeautifulSoup.BeautifulSoup(response.text, features="html.parser")
    listings = soup.find_all("script",type="application/ld+json")[0]
    info = json.loads(listings.text) # convert to json
    return soup, info

def scrape(city, state, code_1, code_2):
    city.replace(" ", "_")
    url = 'https://www.tripadvisor.com/Attractions-{0}-Activities-{1}-{2}_{3}.html'.format(code_1, code_2, city, state)

    if url_to_json(url) is None:
        print("\tError was wrt location: ", city, state)
        return

    activities_list = url_to_json(url)[1]['itemListElement'] # convert to json and get the attractions list

    activities_info = []
    for activity in activities_list: # go to each activity url and get info
        soup, activity_site = url_to_json('https://www.tripadvisor.com' + activity['url'])
        address = activity_site['address']['streetAddress']
        rating = activity_site['aggregateRating']['ratingValue']
        photo = activity_site['image']

        # get reviews, only top 5
        review_text = []
        reviews = soup.find_all("a", href=re.compile("ShowUserReviews(.*?)html"))
        for review in reviews:
            review_link = review['href']
            _, review_site = url_to_json('https://www.tripadvisor.com' + review_link)
            review_text.append(review_site['reviewBody'])

        a = Activity(activity['name'], address, rating, None, photo, "TripAdvisor")
        a.set_tags(review_text)
        activities_info.append(a)

    return activities_info

def tripadvisor_scrape(city, state):
    codes = get_code(city, state)
    results = scrape(city, state, codes[0], codes[1])
    save_json(city + state, results)

# Returns special TripAdvisor codes given city and state
# TODO: find a better way than hardcoding the codes..?
def get_code(city, state):
    # second code can be oa30, oa60, oa90, or oa270 depending on number of results wanted
    # but if set too high, it will redirect to a different URL >:( (90 has been safe for all locations so far)
    codes = {
        "BostonMA" : ["g60745", "oa90"],
        "ProvidenceRI" : ["g60946", "oa90"],
        "NYCNY" : ["g60763", "oa270"],
        "DenverCO" : ["g33388", "oa90"],
        "TampaFL" : ["g34678", "oa90"],
        "HoustonTX" : ["g56003", "oa90"]
        }

    return codes[city+state]

def main():
    locations = [("Boston", "MA", "g60745", "oa60"), ("NYC", "NY", "g60763", "oa270")] # list of (city, state, loc_code, code) tuples
    for loc in locations:
        results = scrape(loc[0], loc[1], loc[2], loc[3])
        save_json(loc[0] + loc[1], results)
    return

if __name__ == '__main__':
    main()

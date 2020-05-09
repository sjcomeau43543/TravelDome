'''
Author:        Eda
Last modified: 5.09.2020 by ez
Status:        Done?

'''
import os, json, requests, re
import bs4 as BeautifulSoup

from activity import Activity

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
        if 'aggregateRating' not in activity_site: # if no rating, set to 0
            rating = None
        else:
            rating = activity_site['aggregateRating']['ratingValue']
        photo = activity_site['image']

        # get reviews, only top 5
        review_text = []
        reviews = soup.find_all("a", href=re.compile("ShowUserReviews(.*?)html"))
        for review in reviews:
            review_link = review['href']
            _, review_site = url_to_json('https://www.tripadvisor.com' + review_link)
            review_text.append(review_site['reviewBody'])

        a = Activity(activity['name'], address, rating, None, photo, "TripAdvisor", link='https://www.tripadvisor.com'+activity['url'], reviews=review_text, tags=[], get_tags=True)
        activities_info.append(a)
        print('added: ', activity['name'])

    return activities_info

def tripadvisor_scrape(city, state):
    codes = get_code(city, state)
    results = scrape(city, state, codes[0], codes[1])
    return results

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
        "HoustonTX" : ["g56003", "oa90"],
        "MontgomeryAL" : ["g30712", "oa90"],
        "JuneauAK" : ["g31020", "oa90"],
        "PhoenixAZ" : ["g31310", "oa90"],
        "LittleRockAR" : ["g60766", "oa90"],
        "SacramentoCA" : ["g32999", "oa90"],
        "HartfordCT" : ["g33804", "oa90"],
        "DoverDE" : ["g34009", "oa90"],
        "TallahasseeFL" : ["g34675", "oa90"],
        "AtlantaGA" : ["g60898", "oa90"],
        "HonoluluHI" : ["g60982", "oa90"],
        "BoiseID" : ["g35394", "oa90"],
        "SpringfieldIL" : ["g60887", "oa90"],
        "IndianapolisIN" : ["g37209", "oa90"],
        "DesMoinesIA" : ["g37835", "oa90"],
        "TopekaKS" : ["g60747", "oa90"],
        "FrankfortKY" : ["g39426", "oa90"],
        "BatonRougeLA" : ["g40024", "oa90"],
        "AugustaME" : ["g29485", "oa90"],
        "AnnapolisMD" : ["g29494", "oa90"],
        "LansingMI" : ["g42391", "oa90"],
        "St.PaulMN" : ["g43501", "oa90"],
        "JacksonMS" : ["g43833", "oa90"],
        "JeffersonCityMO" : ["g44526", "oa90"],
        "HelenaMT" : ["g45212", "oa90"],
        "LincolnNE" : ["g45667", "oa90"],
        "CarsonCityNV" : ["g45926", "oa90"],
        "ConcordNH" : ["g46052", "oa90"],
        "TrentonNJ" : ["g46874", "oa90"],
        "SantaFeNM" : ["g60958", "oa90"],
        "AlbanyNY" : ["g29786", "oa90"],
        "RaleighNC" : ["g49463", "oa90"],
        "BismarckND" : ["g49709", "oa90"],
        "ColumbusOH" : ["g50226", "oa90"],
        "OklahomaCityOK" : ["g51560", "oa90"],
        "SalemOR" : ["g52053", "oa90"],
        "HarrisburgPA" : ["g52787", "oa90"],
        "ProvidenceRI" : ["g60946", "oa90"],
        "ColumbiaSC" : ["g54184", "oa90"],
        "PierreSD" : ["g54760", "oa90"],
        "NashvilleTN" : ["g55229", "oa90"],
        "AustinTX" : ["g30196", "oa90"],
        "SaltLakeCityUT" : ["g60922", "oa90"],
        "MontpelierVT" : ["g57324", "oa90"],
        "RichmondVA" : ["g60893", "oa90"],
        "OlympiaWA" : ["g58653", "oa90"],
        "CharlestonWV" : ["g58947", "oa90"],
        "MadisonWI" : ["g60859", "oa90"],
        "CheyenneWY" : ["g60439", "oa90"]
        }

    return codes[city+state]

def main():
    locations = [("Boston", "MA", "g60745", "oa60"), ("NYC", "NY", "g60763", "oa270")] # list of (city, state, loc_code, code) tuples
    for loc in locations:
        results = scrape(loc[0], loc[1], loc[2], loc[3])
        #save_json(loc[0] + loc[1], results)
    return

if __name__ == '__main__':
    main()

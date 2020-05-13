# TravelDome

Welcome to TravelDome, a multi-activity itinerary generator with personality matching.

Created by: Samantha Comeau, Eda Zhou and Gordon Zhang.

## Key takeaways
There were two main goals to this project.

1. to create a place to store multiple activities
2. to match a user's personality to the activities that they would like most

We consider the first a success. We successfully created a place for users to easily see and change their itinerary for a trip with no sponsored ads, and a simple UI that focuses on the activities themselves. We didn't bog the UI with reviews, and other data, but provided a link to multiple sources where the user can find more information instead. We maintained our simplistic UI but accomplished this goal at the same time.

We consider the second a success as well. Using reviews to match the user's personality was a success because we believe that due to the adjectives success in describing the locations we were able to recommend lesser known activities to the user. Rather than seeing the UI bogged with chains like Taco Bell, the user rather gets a better recommendation and the opportunity to support a smaller business in most cases. The main area of improvement in this section would be to quality test the results better. Comparing these results to an existing engine does not do it justice, since many engines do not handle adjectives well. For example, compared to Google we successfully recommended 1/5 of the places that Google would have recommended to the user.

## Structure

| directory | purpose |
|-----------|---------|
| ./data    | store the activity, cluster, inverted index data|
| ./data_manipulation | scripts to manipulate the raw data scraped |
| ./GoogleMapsPhotoLibrary | the images from google maps |
| ./quality | output of the quality script to be analyzed manually |
| ./scrapers | all the information for the scraping scripts |
| ./visualizations | some intermediate visualizations used to analyze the frequency of our adjectives |
| ./website | the design and backend for the website |
| .gitignore | the gitignore |
| index.html | the main file loaded as the bones of the website |
| README.md | this readme |
| requirements.txt | the required python packages for running the scripts. We used Python3.6 |

## Setup virtual environment
Create a python virtualenvironment using the following commands.

```
python3 -m pip install virtualenv
mkdir TravelDome/venv
python3 -m venv TravelDome/venv
cd TravelDome
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

This will install the required packages for running the scrapers and the rest of the data.

### Optional
To run a local instance of the website you can do the following.

1. Change the flag for production in website/js/index.js to false.
2. Run the following

```
git clone https://github.com/sjcomeau43543/secure_server
cd TravelDome
python3 ../secure_server/secure_server.py -d .
```

Then you can access the website at 127.0.0.1:7001 by default.

## Data

You can find all of our integral data in the `data` directory. Each directory is clearly labelled as the source / meaning of the data. The `GoogleMapsPhotoLibrary` are the photos from GoogleMaps. Yelp, TripAdvisor, and NPS provided image urls which were used to display those images.

## Data Collection

### Scrape data
First, we needed to scrape activity information.

[Scraping script](scrapers/scrape.py)

This script will scrape Yelp, TripAdvisor, National Parks Service, and GoogleMaps depending on the flags you provide it. For example, to run them all you would run 
```
python3 scrape.py -y -c YELPCONFIG -n -g -t -l locations.txt -o
```

The yelp configuration for the REST API is not provided on github, since this is a public repository. 
To gain your own Yelp credentials apply for an application on the Fusion developers website.

## Data Manipulation

Alternatively to running all these scripts separately, you can run the bash script `runall.sh`.
```
./runall.sh
```

### Merge data
Next, we needed to store this data in one place for each location so we could merge the results that were the same from multiple sites. 

[Merging script](data_manipulation/merge.py)

This script will walk the `data` repository for the `Yelp`, `TripAdvisor`, `NPS`, and `GoogleMaps` folders and the location data inside them. The merged results for each location are then stored in the `Merged` directory. A sample run looks like 
```
python3 merge.py -l ../scrapers/locations.txt
```

### Store data
After merging the data, it needs to be stored in an inverted index for easy lookups.

[Inverted Index](data_manipulation/storage.py)

This script will convert the documents in the `data/Merged` folder into a single inverted index which is then stored in `data/InvertedIndex`. For each adjective in the provided adjectives file (either extended or standard) the activities that are tagged with that location are stored in the index as the documents. A sample run looks like 
```
python3 storage.py -l ../scrapers/locations.txt -a ../scrapers/adjectives_extended.txt
``` 

### KNN 
The inverted index is only used for the first round of results to the user. Using the positive feedback we need to recommend similar activities to the one that was chosen.

[KNN](data_manipulation/clustering.py)

This script will vectorize the activities in the `data/Merged` folder as vectors of the adjectives with 1 if the activity has that adjective as a tag and 0 otherwise. Then the euclidean distances are calculated between all of the activities and pre-recorded so that this does not have to be calculated during query time. The results are stored in `data/Cluster`. A sample run looks like 
```
python3 clustering.py -l ../scrapers/locations.txt -e ../scrapers/adjectives_extended.txt -n 5
```

## Website 

The only change needed to run a local instance of the website is in the `loadFile()` function where it references the filepath to the data files. Using this repository, [Secure Server](https://github.com/sjcomeau43543/secure_server), you can run `python3 secure_server.py -d TravelDome/` to run a local instance.

### Querying data
Data querying is handled in `Javascript`.

The functions used to query data are `generateRecommendations()`, `generateSecondaryRecommendations()`, `loadAdjectives()`, and `loadLocations()`. All our data is loaded using the `loadData()` function.

### Ranking data
Originally the plan was to rank data before the actual query. However, we found it simpler and speedy enough to do this on the fly. Data ranking is handled in the `rank()` function in javascript. We only return the top 10 results because it simplifies the User Interface.

### Displaying data
A combination of `html`, `css`, `javascript`, and `Bootstrap` were used to produce the frontend for the user.

### Visit website
[TraveDome](https://sjcomeau43543.github.io/TravelDome)
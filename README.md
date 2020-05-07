# TravelDome

## Workflow

### Scrape data
First, we needed to scrape activity information.

[Scraping script](scrapers/scrape.py)

This script will scrape Yelp, TripAdvisor, and GoogleMaps depending on the flags you provide it. For example, to run them all you would run 
```
python3 scrape.py -y -c YELPCONFIG -g -t -l locations.txt -o
```

The yelp configuration for the REST API is not provided on github, since this is a public repository. 

### Merge data
Next, we needed to store this data in one place for each location so we could merge the results that were the same from multiple sites. 

[Merging script](data_manipulation/merge.py)

This script will walk the `data` repository for the `Yelp`, `TripAdvisor` and `GoogleMaps` folders and the location data inside them. The merged results for each location are then stored in the `Merged` directory. A sample run looks like 
```
python3 merge.py ../scrapers/locations.txt
```

### Store data
After merging the data, it needs to be stored in an inverted index for easy lookups.

[Inverted Index](data_manipulation/storage.py)

This script will convert the documents in the `data/Merged` folder into a single inverted index which is then stored in `data/InvertedIndex`. For each adjective in the provided adjectives file (either extended or standard) the activities that are tagged with that location are stored in the index as the documents. A sample run looks like 
```
python3 storage.py -l ../scrapers/locations.txt -a ../scrapers/adjectives.txt
``` 

### KNN 
The inverted index is only used for the first round of results to the user. Using the positive feedback we need to recommend similar activities to the one that was chosen.

[KNN](data_manipulation/clustering.py)

This script will vectorize the activities in the `data/Merged` folder as vectors of the adjectives with 1 if the activity has that adjective as a tag and 0 otherwise. Then the euclidean distances are calculated between all of the activities and pre-recorded so that this does not have to be calculated during query time. The results are stored in `data/Cluster`. A sample run looks like 
```
python3 clustering.py -e ../scrapers/adjectives_extended.txt -n 5
```

### Querying data
Finally, queries can be made to our model.

[Query](data_manipulation/query.py)

Given a query, this script will return activities ranked from most to least relevant. The query must be in the form ["location", "adjective1", "adjective2", ...] where the adjectives are the main adjectives. For example: `["BostonMA", "frugal", "foodie", "creative"]`. First, their synonyms are obtained from the `/scrapers/adjectives_extended.txt` file. Then, using the inverted index at `data/InvertedIndex`, a list of activities names that match at least one of the adjectives and the location is computed. Finally, they are ranked according on their scores: 1 pt for each occurrence of main adjective and .5 for each occurrence of secondary adjective in the activity's tag list.
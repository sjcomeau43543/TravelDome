'''
Author:        Eda
Last modified: 4.29.2020 by sjc
Status:        Depreciated, moved to activity.py, left here in case we need to cross reference

TODO: add tags to GoogleMaps data
'''
'''import os, json, string

# Returns list of adjectives (from adjectives file) that appear in the given list of reviews
# If an adjective appears in multiple reviews, there will be that many instances of
# the adjective in the tag list. However, multiple occurances in the SAME review will
# not be counted
def get_tags(reviews):
    with open('../scrapers/adjectives_extended.txt', 'r') as f:
        adjs = [adj.strip(',') for adj in f.read().split()]

    tags = []
    for review in reviews:
        words = set([w.strip(string.punctuation) for w in review.split()]) # get unique words in a list with no end punctuation
        tags.extend(list(words & set(adjs))) # get common words and add to tags

    #tags = list(filter(None, tags)) # remove empty lists
    return tags

# Given directory (with json files), adds tags the json files and saves them as new files
def tag_dir(dir):
    for filename in os.listdir(dir):
        with open(dir + filename, 'r') as j:
            data = json.load(j)
            for entry in data: # get and set tags
                tags = get_tags(entry['reviews'])
                entry['tags'] = tags
            with open(dir + 'tagged_' + filename, 'a+') as nf: # save data w/tags to new file
                json.dump(data, nf, indent=1)

def main():
    directories = ['../data/TripAdvisor/', '../data/Yelp/'] # TODO: Do google
    for dir in directories:
        tag_dir(dir)

    return

if __name__ == '__main__':
    main()
'''
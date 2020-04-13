class Activity:
    
    name = ""
    address = ""
    hours = {"Sunday":"", # use datetime objects
             "Monday":"",
             "Tuesday":"",
             "Wednesday":"",
             "Thursday":"",
             "Friday":"",
             "Saturday":""}
    avg_visitor_review = 0.0
    avg_time_spent = 0 # in minutes
    photo_location = "" # filename in pictures directory
    tags = [] # list of tags from scraping user reviews

    def __init__(self):
        pass

    # pass in top reviews
    def get_tags(self, reviews):
        for review in reviews:
            pass
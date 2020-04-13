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

    def __init__(self, name, address, hours, avg_visitor_review, avg_time_spent, photo_location):
        self.name = name,
        self.address = address
        for hour,day in zip(hours,self.hours.keys()):
            self.hours[day] = hour
        self.avg_visitor_review = avg_visitor_review
        self.avg_time_spent = avg_time_spent
        self.photo_location = photo_location

    # pass in top reviews
    # TODO
    def set_tags(self, reviews):
        for review in reviews:
            pass
import json
import tweepy
import botometer
from progress.bar import Bar
import time
import os
from dotenv import load_dotenv

# steps

# authentication function

# get data through tweepy function

# analyze data through botometer (bonus with progress bar)

# save data into a json file

def getdata(query, size, sub): 
    load_dotenv()
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    RAPID_API_KEY = os.getenv('RAPID_API_KEY')
    
    # Authenticate the twitter/tweepy tokens
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # set the API
    api = tweepy.API(auth)
    twitterauth = {
        'consumer_key': CONSUMER_KEY,
        'consumer_secret': CONSUMER_SECRET,
        'access_token': ACCESS_TOKEN,
        'access_token_secret': ACCESS_TOKEN_SECRET,
    }

    # Authenticate the rapid API tokens
    rapidapi = RAPID_API_KEY

    # set botometer
    bom = botometer.Botometer(rapidapi_key=rapidapi,**twitterauth)

    # pull the data requested
    pulldata = tweepy.Cursor(api.search, q=query, lang='en',).items(size)

    # keep track of the users being addressed
    users = []

    # reference on how to parse this response: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
    # put the usernames into an array
    for i in pulldata:
        users.append(i.user.screen_name)

    bar = Bar('Analyzing...', max = size)
    bar.start()
    data = []
    # iterate through the list of users and check each individually, then track info needed for average
    for user in users:
        # temporary variable to save details of the current user botometer check
        hold = bom.check_account(user)
        data.append(hold['display_scores']['english'])
        bar.next()
    bar.finish()

    # set the name for the file in the format query, size of the data, and then the date and time it's been received
    name = query + '-' + str(size) + '-' + time.strftime("%Y%m%d-%H%M%S")
    if sub != "": 
        query = query + "-" + sub

    # make a folder to store the data if needed
    if not os.path.exists("data"):
        os.makedirs("data")

    # make a new folder for a new query if needed
    if not os.path.exists("data/{}".format(query)):
        os.makedirs("data/" + query)

    with open("data/{}/{}.json".format(query, name), 'w') as outfile: 
        json.dump(data, outfile, indent=4)
import tweepy
import botometer
import pandas as pd
from dotenv import load_dotenv
import os

# load the key variables from the .env file
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# Authenticate the twitter/tweepy tokens
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Authenticate the rapid API tokens
rapidapi = RAPID_API_KEY

# set the API
api = tweepy.API(auth)
twitterauth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_TOKEN,
    'access_token_secret': ACCESS_TOKEN_SECRET,
  }

# set botometer
bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=rapidapi,**twitterauth)

# take an input of the desired search
print('Enter requested topic search: ')
query = input()
print('Enter requested sample size: ')
size = int(input())

# pull the data requested
pulldata = tweepy.Cursor(api.search, q=query, lang='en',).items(size)

# keep track of the users being addressed
users = []

# keep track of the different scores
# results can be explained here: https://github.com/IUNetSci/botometer-python
overall = []
astroturf = []
fake_follower = []
financial = []
other = []
self_declared = []
spammer = []

# reference on how to parse this response: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
# print the usernames for testing purposes and put them into an array
for i in pulldata:
  users.append(i.user.screen_name)
  print(i.user.screen_name)

# to generate the average score
count = 0
overnum = 0
astronum = 0
fakenum = 0
finnum = 0
othnum = 0
selfnum = 0
spamnum = 0

# iterate through the list of users and check each individually, then track info needed for average
for user in users:
  # temporary variable to save details of the current user botometer check
  hold = bom.check_account(user)
  # append each score
  overall.append(hold['display_scores']['english']['overall'])
  astroturf.append(hold['display_scores']['english']['astroturf'])
  fake_follower.append(hold['display_scores']['english']['fake_follower'])
  financial.append(hold['display_scores']['english']['financial'])
  other.append(hold['display_scores']['english']['other'])
  self_declared.append(hold['display_scores']['english']['self_declared'])
  spammer.append(hold['display_scores']['english']['spammer'])

  # generate the average score for each bot score
  count = count + 1
  overnum = overnum + float(hold['display_scores']['english']['overall'])
  astronum = astronum + float(hold['display_scores']['english']['astroturf'])
  fakenum = fakenum + float(hold['display_scores']['english']['fake_follower'])
  finnum = finnum + float(hold['display_scores']['english']['financial'])
  othnum = othnum + float(hold['display_scores']['english']['other'])
  selfnum = selfnum + float(hold['display_scores']['english']['self_declared'])
  spamnum = spamnum + float(hold['display_scores']['english']['spammer'])

# calculate the average
aveover = overnum / count
aveastro = astronum / count
avefake = fakenum / count
avefin = finnum / count
aveoth = othnum / count
aveself = selfnum / count
avespam = spamnum / count

# put the user data and scores into a data frame
userdata = pd.DataFrame({'User': users, 'Overall Score': overall, 'Astroturf Score': astroturf, 'Fake Follower Score': fake_follower, 
  'Financial Score': financial, 'Other Score': other, 'Self Declared Score': self_declared, 'Spammer Score': spammer})

print(userdata)

print("\nThe average overall bot score is: " + str(round(aveover, 3)))
print("\nThe average astroturf bot score is: " + str(round(aveastro, 3)))
print("\nThe average fake follower bot score is: " + str(round(avefake, 3)))
print("\nThe average financial bot score is: " + str(round(avefin, 3)))
print("\nThe average other bot score is: " + str(round(aveoth, 3)))
print("\nThe average self delcared bot score is: " + str(round(aveself, 3)))
print("\nThe average spammer bot score is: " + str(round(avespam, 3)))  
import re
import csv
import tweepy
import pandas as pd

csv.field_size_limit(2 ** 16)

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Specify Twitter Handles to collect
#infile = pd.read_csv('Leader Twitter Handles.csv')
#users = infile['Handle']
users = ["JoeBiden"]

# Set up Pandas Data Frame for data
col_names = ['User', 'ID', 'DateTime', 'Device', 'Retweets', 'Likes', 'Text']
tweets = pd.DataFrame(columns=col_names)
n = 1

#Use Cursor method to get statuses
for user in users:
    print(user)
    for status in tweepy.Cursor(api.user_timeline, id = user, tweet_mode='extended').items():
        tweets.loc[n,"User"] = user
        tweets.loc[n,"ID"] = status.id
        tweets.loc[n,"DateTime"] = status.created_at
        tweets.loc[n,"Device"] = status.source
        tweets.loc[n,"Retweets"] = status.retweet_count
        tweets.loc[n,"Likes"] = status.favorite_count
        text = status.full_text.replace("\n", " ").replace("\r\n", " ")
        tweets.loc[n,"Text"] = text
        n = n+1

#Write pandas df to csv
tweets.to_csv("Practice Tweets.csv")



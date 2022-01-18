import csv
import tweepy
import pandas as pd
import time
csv.field_size_limit(2 ** 16)

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Specify keywords in desired tweets
terms = ['election2020','democrats', 'republicans']

# Set up Pandas Data Frame for data
col_names = ['Term', 'ID', 'DateTime', 'Username', 'Retweets', 'Likes', 'Text']
tweets = pd.DataFrame(columns=col_names)
n = 1
max_tweets = 5000
first = True
while True:
    for term in terms:
        while n < max_tweets:
            print(n)
            try:
                #Change since parameter to desired dates (note: only past ~3 weeks is generally possible)
                for status in tweepy.Cursor(api.search,q=terms,lang="en",since="2020-10-01",tweet_mode='extended').items():
                    tweets.loc[n, "Term"] = term
                    tweets.loc[n, "ID"] = status.id
                    tweets.loc[n, "DateTime"] = status.created_at
                    tweets.loc[n, "Username"] = status.author.screen_name
                    tweets.loc[n, "Retweets"] = status.retweet_count
                    tweets.loc[n, "Likes"] = status.favorite_count
                    text = status.full_text.replace("\n", " ").replace("\r\n", " ")
                    tweets.loc[n, "Text"] = text
                    n = n + 1
            except:
                time.sleep(60)

    if first is True:
         # Write pandas df to csv, change both filenames to output file
        tweets.to_csv("practice.csv")
        first = False
    else:
        tweets.to_csv("practice.csv", mode = 'a', header = False)

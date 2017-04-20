import sys
import os
import json
import tweepy
import csv
import geocoder
import time
import datetime

## API 
consumer_key = "TxS1uoRG2BFU9zhCmqKT4xYls"
consumer_secret = "cmGgvhIyxU1ULD1Sudh6HsRAstMYixrXrOf9cdqcW7C3JiyH0u"
access_token = "328921730-LHlmQASsKLD5mC8bcfPAP6sPseZwBy0SfGvrovPG"
access_toke_secret = "r8oUb8JAlLEmijUMKmZlDUQmyJWw5ywoJruUzR0bESUy4"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_toke_secret)
api = tweepy.API(auth) #, retry_count = 10, wait_on_rate_limit=True, wait_on_rate_limit_notify = True)


##creating CSV file
outfile = 'nyu_data.csv'
csvfile = open(outfile, 'w', encoding = 'utf-8', errors='ignore')
csvwriter = csv.writer(csvfile)
row = ['user', 'created_at', 'latitude', 'longitude', 'text']
csvwriter.writerow(row)

#location searching
location = 'New york city'
g = geocoder.google(location)
place = api.geo_search(query = location, granularity = 'city')
place_id = place[0].id
print(location, 'id is:', place_id)


#search query
query = 'place:' + place_id + ' + ' + 'NYU OR Columbia'
print('Searching: ' + query)

#search loop
max_results = 150
results = 0
max_id = None

while results < max_results:
    try:
        searchtweet = tweepy.Cursor(api.search, q = query,
                                    max_id = max_id).items()
        tweet = searchtweet.next()
        if not searchtweet:
            print('no tweets found')
            break
        max_id = tweet.id-1
        
        #format tweet into workable dictionary
        t = json.loads(json.dumps(tweet._json))

        ## create elements to save
        user = t['user']['screen_name']
        created_at = t['created_at']
        text = "'"+t['text']+"'"
        ## if coordinates exist, save them
        if tweet.coordinates != None:
            lat = tweet.coordinates['coordinates'][1]
            lon = tweet.coordinates['coordinates'][0]
        else:
            lat = None
            lon = None
        addrow = [user, created_at, lat, lon, text]
        csvwriter.writerow(addrow)
        results +=1
        
    except tweepy.TweepError:
        print('exception raised, waiting 15 min, found {0} tweets'.format(results))
        time.sleep(15*60)
    except StopIteration:
        break

csvfile.close()
print('downloaded {0} tweets'.format(results))

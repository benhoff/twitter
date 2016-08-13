import os
from time import sleep
import twitter

from twython import Twython


"""
oauth = twitter.OAuth(access_token_key, access_token_secret, consumer_key,
        consumer_secret)

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

stream = twitter.TwitterStream(auth=oauth)

for value in stream.statuses.sample():
    print(value)
    sleep(.75)

"""
# twitter = Twython(consumer_key, consumer_secret, oauth_version=2)
# twitter = Twython(consumer_key, consumer_secret)
twitter = Twython(access_token_key, access_token_secret)
auth = twitter.get_authentication_tokens()
print(auth)
# twitter = Twython(consumer_key, consumer_secret)
twitter.verify_credentials()


# TODO: Should probably save using pickle
# ACCESS_TOKEN = twitter.obtain_access_token()
# twitter = Twython(consumer_key, access_token=ACCESS_TOKEN)

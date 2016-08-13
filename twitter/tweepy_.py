import os
import json
import time
import asyncio
from time import sleep

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob.classifiers import NaiveBayesClassifier


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

def _set_value_if_none_from_environment(value, name):
    if value == '':
        envirnoment = os.getenv(name)
        if envirnoment is None:
            print('{} not set in environment or script!'.format(name))
        return envirnoment

# oauth consumer key
consumer_key = _set_value_if_none_from_environment(consumer_key,
                                                   'consumer_key')

# 
consumer_secret = _set_value_if_none_from_environment(consumer_secret,
                                                      'consumer_secret')

access_token_secret = _set_value_if_none_from_environment(access_token_secret,
                                                          'access_token_secret')

access_token = _set_value_if_none_from_environment(access_token,
                                                   'access_token_key')

class StdOutListener(StreamListener):
    def __init__(self):
        self.last_tweet_printed = time.time()
        self.classified = False

    def on_data(self, data):
        if not self.classified:
            data = json.loads(data)
            print(data.keys())
        else:
            time_now = time.time()
            if time_now - self.last_tweet_printed > 1:
                data = json.loads(data)
                print('{}: {}\n'.format(data['user']['screen_name'], data['text']))
                self.last_tweet_printed = time_now
        return True

    def on_error(self, status):
        print(status)

class ClassifierListener(StreamListener):
    def __init__(self, category):
        self.trained = False
        self.data_reached = False
        self.category = category
        self.target_data_number = 25000
        self.training_data = []
        self._training_data_number = 0

    def on_data(self, data):
        if not self.trained and not self.data_reached:
            data = json.loads(data)
            if not data.get('retweeted', True):
                self.training_data.append(data['text'])
                self._training_data_number += 1
                print(self.category, self._training_data_number)

                if self._training_data_number > self.target_data_number:
                    self.data_reached = True
                    return False

            return True
        return False

class ClassifyData(StreamListener):
    def __init__(self, classifier):
        self.classifer = classier
        self.classifier_labels = self.classifer.labels()

    def on_data(self, data):
        data = json.loads(data)
        probability = self.classifer.prob_classify(data['text'])
        print('{}: {}'.format(data['user']['screen_name'], data['text']))
        for k in self.classifier_labels:
            print(k, probability.prob(k))
        print('\n')

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    kenny_listener = ClassifierListener('kenny')
    hilliary_listner = ClassifierListener('hillary')
    olympics_listner = ClassifierListener('olympics')
    trump_listner = ClassifierListener('trump')

    kenny_stream = Stream(auth, kenny_listener)
    hillary_stream = Stream(auth, hilliary_listner)
    olympics_stream = Stream(auth, olympics_listner)
    trump_stream = Stream(auth, trump_listner)


    listener_list = [kenny_listener, hilliary_listner, olympics_listner, trump_listner]

    kenny_stream.filter(track=['kenny'], async=True)
    hillary_stream.filter(track=['hillary'], async=True)
    olympics_stream.filter(track=['olympics'], async=True)
    trump_stream.filter(track=['trump'], async=True)


    blocking_call = input('press enter when ready')


    training_data = []
    for listener in listener_list:
        listener.data_reached = True
        for data in listener.training_data:
            training_data.append((data, listener.category))

    print('training classifier!')
    classier = NaiveBayesClassifier(training_data)
    print('classifier trained!')

    classifer_listener = ClassifyData(classier)
    olympics_stream = Stream(auth, classifer_listener)

    olympics_stream.filter(track=['olympics',
                                  'hillary',
                                  'kenny',
                                  'trump'])

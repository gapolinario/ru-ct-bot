# coding: utf-8

import tweepy
from datetime import datetime
import sys

# Tweepy docs
# http://docs.tweepy.org/en/v3.5.0/api.html

# Import our Twitter credentials from credentials.py
# See format for this file on blank_credentials.py
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# input is Almoço or Jantar
meal = sys.argv[1]

now=datetime.now()
title = "{0:s}_{1:d}_{2:s}_{3:d}_{4:s}".format(now.strftime("%a"), now.day,now.strftime("%B"), now.year, meal[:3])

api.update_with_media("data/"+title+'.png')

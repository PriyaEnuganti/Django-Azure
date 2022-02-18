
import pandas as pd
import numpy as np
import nltk
import re
import emoji
import matplotlib.pyplot as plt
import sklearn
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('stopwords');
nltk.download('punkt');
nltk.download('omw-1.4');
import contractions
import unidecode

def remove_retweet(tweet):
    tweet = re.sub('RT\s+', '', tweet)
    return tweet
def remove_numbers(tweet):
    return  re.sub(r'[0-9]+', '',tweet)
def remove_greek(tweet):
    return unidecode.unidecode(tweet)
def remove_user_tag(tweet):
    tweet = re.sub('\B@\w+', '', tweet)
    return tweet
def decode_emoji(tweet):
    tweet = emoji.demojize(tweet)
    return tweet
def remove_url(tweet):
    tweet = re.sub('(http|https):\/\/\S+', '', tweet)
    return tweet
def remove_hashtag(tweet):
    tweet = re.sub(r'#+', '', tweet)
    return tweet
def to_lowercase(tweet):
    tweet = tweet.lower()
    return tweet
def remove_special_char(tweet):
    tweet = re.sub(r'[^A-Za-z]+\s?', ' ', tweet)
    return tweet
def remove_short_char(tweet):
    tweet = re.sub(r'\b\w{1,2}\b', ' ', tweet)
    return tweet
def contraction_expand(tweet):
    tweet = contractions.fix(tweet)
    return tweet
stop_words = set(nltk.corpus.stopwords.words('english'))
def tokenize_tweet(tweet):

  token_list = word_tokenize(tweet)
  stopwords = nltk.corpus.stopwords.words('english')

  # adding twitter specific stop words
  new_stopwords = ["amp", "sm1", 'smh', 'idk', 'idc', 'lol', 'lmao', 'btw', 'fml', 'fyi', 'ftw', 'ftl', 'icymi', 'mtf'
                  ,'tbh', 'tbt', 'wtv', 'might', 'new']
  stopwords.extend(new_stopwords)
  token_list = [token for token in token_list if not token in stopwords]

  return token_list
  
def lemmatize_tweets(tokens,lemmatizer):
  token_list = []
  for token in tokens:
    token_list.append(lemmatizer.lemmatize(token))
  return token_list
##### Tweet pre-processing
def preprocess_tweet(tweet):

  # Cleaning tweets
  tweet = remove_retweet(tweet)
  tweet=remove_numbers(tweet)
  tweet=remove_greek(tweet)
  tweet = remove_user_tag(tweet)
  tweet = remove_url(tweet)
  tweet = remove_hashtag(tweet)
  tweet = decode_emoji(tweet)

  # Handling word-features
  tweet = to_lowercase(tweet)
  tweet = contraction_expand(tweet)
  tweet = remove_special_char(tweet)
  tweet = remove_short_char(tweet)

  # Tokenizing & Lemmatizing
  tokens = tokenize_tweet(tweet)
  tweet_lemmatizer = WordNetLemmatizer();
  lemma = lemmatize_tweets(tokens, tweet_lemmatizer)

  return lemma

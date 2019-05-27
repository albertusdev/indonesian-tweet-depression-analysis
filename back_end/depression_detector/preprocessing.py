import pandas as pd

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize

import re


stop_factory = StopWordRemoverFactory()
more_stopword = ['rt', 'dengan', 'ia', 'bahwa', 'oleh']

# Add more Stopwords
stop_words = stop_factory.get_stop_words() + more_stopword

# Create StopWord Removal using our own Stop words
stop_word_remover = StopWordRemover(ArrayDictionary(stop_words))

# Create stemmer
stemmer = StemmerFactory().create_stemmer()

PATH_TO_KEY_NORM_FILE = './dictionary/key_norm.csv'

key_norm = pd.read_csv(PATH_TO_KEY_NORM_FILE).drop(['_id'], axis=1)
key_norm_dict = {key_norm['singkat'][i]: key_norm['hasil'][i] for i in range(len(key_norm))}


def formalize(word):
    if word in key_norm_dict:
        return key_norm_dict[word]
    return word


def preprocess_tweet(tweet, debug=False):
    if debug: print(tweet, end="\n\n")

    # Lower casing
    clean_tweet = tweet.lower()  # lowercase

    # URL Removal and Username removal
    clean_tweet = re.sub(r"(?:\@|https?\://)\S+", " ", clean_tweet)
    if debug: print('After URL and username removal: ', clean_tweet, end="\n\n")

    # Punctuation removal
    clean_tweet = re.sub(r'[^\w\s]', ' ', clean_tweet)
    if debug: print('After punctuation removal: ', clean_tweet, end="\n\n")

    # Extra space removal
    clean_tweet = re.sub('\s+', ' ', clean_tweet)
    if debug: print('After extra space removal: ', clean_tweet, end="\n\n")

    # Trimming
    clean_tweet = clean_tweet.strip()
    if debug: print('After trimming: ', clean_tweet)

    # Transforming informal words to formal words
    clean_tweet = " ".join([formalize(word) for word in word_tokenize(clean_tweet)])
    if debug: print('After transforming informal words: ', clean_tweet, end="\n\n")

    # Stop words removal
    clean_tweet = stop_word_remover.remove(clean_tweet)
    if debug: print('After stop words removal: ', clean_tweet, end="\n\n")

    # Stemming
    clean_tweet = stemmer.stem(clean_tweet)
    if debug: print('After stemming: ', clean_tweet, end="\n\n")

    if debug: print()

    return clean_tweet

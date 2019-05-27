import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer


class FeatureSelector:
    def __init__(self, dataset):
        self.bow_transformer = CountVectorizer().fit(dataset["cleaned"])
        self.tf_idf_transformer = TfidfVectorizer().fit(dataset["cleaned"])

    def extract_tf_idf(self, tweet_list):
        return self.tf_idf_transformer.transform(np.array(tweet_list)).toarray()

    def extract_bag_of_words(self, tweet_list):
        return self.bow_transformer.transform(np.array(tweet_list)).toarray()

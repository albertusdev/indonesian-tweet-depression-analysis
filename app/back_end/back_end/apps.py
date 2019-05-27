import pandas as pd
import nltk

from django.apps import AppConfig

from back_end.depression_detector.model import Classifier
from back_end.depression_detector.feature_selection import FeatureSelector
from .depression_detector.preprocessing import key_norm_dict


class App:
    PATH_TO_KEY_NORM_FILE = '../../dictionary/key_norm.csv'
    PATH_TO_CLEANED_DATASET = '../../labeled_dataset_cleaned.csv'

    classifier = None

    @staticmethod
    def start():
        global key_norm_dict

        def read_key_norm():
            global key_norm_dict
            key_norm = pd.read_csv(App.PATH_TO_KEY_NORM_FILE).drop(['_id'], axis=1)
            key_norm_dict = {key_norm['singkat'][i]: key_norm['hasil'][i] for i in range(len(key_norm))}

            return key_norm_dict

        def read_dataset():
            return pd.read_csv(App.PATH_TO_CLEANED_DATASET)

        print("Getting ready...")
        nltk.download('punkt')
        nltk.download('stopwords')

        print("Reading Key Norms from file...")
        read_key_norm()
        print('Keynorm len: ', len(key_norm_dict))

        dataset = read_dataset()
        print('Dataset len: ', len(dataset))

        print("Training models begin...")
        App.classifier = Classifier(feature_selector=FeatureSelector(dataset))
        App.classifier.train(dataset)

        print("Training finish...")

        print("Testing 5 predictions... ")

        for _, row in dataset.head().iterrows():
            tweet, label = row['tweet'], row['is_depressed']

            print(App.classifier.predict(tweet), label)

import pandas as pd
import nltk


from back_end.depression_detector.model import Classifier
from back_end.depression_detector.feature_selection import FeatureSelector


class App:
    PATH_TO_CLEANED_DATASET = './labeled_dataset_cleaned.csv'

    classifier = None

    @staticmethod
    def start():

        def read_dataset():
            return pd.read_csv(App.PATH_TO_CLEANED_DATASET)

        print("Getting ready...")
        nltk.download('punkt')
        nltk.download('stopwords')

        print("Reading Key Norms from file...")

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

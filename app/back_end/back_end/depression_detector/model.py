import numpy as np

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from .preprocessing import preprocess_tweet


class Classifier:
    def __init__(self, feature_selector):
        self.models = [
            KNeighborsClassifier(2),
            DecisionTreeClassifier(),
            LinearSVC(),
            LogisticRegression(solver='lbfgs'),
        ]
        self.feature_selector = feature_selector

    def train(self, dataset):
        models = []
        feature, label = self.feature_selector.extract_tf_idf(dataset['cleaned']), dataset['is_depressed']
        for classifier in self.models:
            print("Training " + classifier.__class__.__name__ + "...")
            models.append(classifier.fit(feature, label))
            scores = cross_val_score(classifier, feature, label, cv=7)
            print("Result: ", scores.mean())

        self.models = models
        return self.models

    def predict(self, text):
        text = preprocess_tweet(text)
        feature = self.feature_selector.extract_tf_idf([text])
        result = {}
        for classifier in self.models:
            result[classifier.__class__.__name__] = classifier.predict(feature)[0]
        return result

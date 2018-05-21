import re
import math
import itertools
import collections
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


class Sentiment:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def feature_dict(self, words):
        return dict([(word, True) for word in words])

    def create_sets(self, featuredict):

        categories_dict = {'sad': {'features':[], 'datapath': os.path.join(self.folder_name, 'sad')},
                        'calm': {'features':[], 'datapath': os.path.join(self.folder_name, 'calm')},
                        'energetic': {'features':[], 'datapath': os.path.join(self.folder_name, 'energetic')}}

        for key in categories_dict:
            with open(categories_dict[key][datapath], 'r') as datalist:
                for data in datalist:
                    words = re.findall(r"[\w']+ | [.,!?;]", data.rstrip())

                    words = [featuredict(words), key]
                    categories_dict[key]['features'].append(words)



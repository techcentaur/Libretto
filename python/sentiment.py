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

        categories_dict = {'sad': {'features':[], 'datapath': os.path.join(self.folder_name, 'sad'), 'cutoff': 0.0},
                        'calm': {'features':[], 'datapath': os.path.join(self.folder_name, 'calm'), 'cutoff': 0.0},
                        'energetic': {'features':[], 'datapath': os.path.join(self.folder_name, 'energetic'), 'cutoff': 0.0}}

        for key in categories_dict:
            with open(categories_dict[key][datapath], 'r') as datalist:
                for data in datalist:
                    words = re.findall(r"[\w']+ | [.,!?;]", data.rstrip())

                    words = [featuredict(words), key]
                    categories_dict[key]['features'].append(words)

        for key in categories_dict:
            categories_dict[key]['cutoff'] = int(math.floor(len(categories_dict[key]['features']) * 0.75))

        for key in categories_dict:
            train_features.append((categories_dict[key]['features'])[:(categories_dict[key]['cutoff'])]) 
            test_features.append((categories_dict[key]['features'])[(categories_dict[key]['cutoff']):]) 
        
        return {'train': train_features, 'test': test_features}

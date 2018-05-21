import re
import math
import itertools
import collections
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


class Sentiment:
    def __init__(self, folder_name, execute):
        self.folder_name = folder_name
        self.execute = execute #['print', 'json']

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

    
    def machine_model(self, data_dict):

        classifier = NaiveBayesClassifier.train(data_dict['train'])

        reference_set = collections.defaultdict(set)
        test_set = collections.defaultdict(set)

        for i, (features, key) in enumerate(data_dict['test']):
            reference_set[key].add(i)

            predict = classifier.classify(features)
            test_set[predict].add(i)

        if self.execute is 'print':
            
            print('Trained on {trainf} instances and tested on {testf} instances ...'.format(trainf=len(data_dict['train']), testf=len(data_dict['test'])))
            print('Accuracy:', nltk.classify.util.accuracy(classifier, data_dict['test']))
            
            print('/------------------- SAD ------------------/')
            print('Precision:', nltk.metrics.precision(reference_set['sad'], test_set['sad']))
            print('Recall:', nltk.metrics.recall(reference_set['sad'], test_set['sad']))
            
            print('/------------------- CALM -------------------/')
            print('Precision:', nltk.metrics.precision(reference_set['calm'], test_set['calm']))
            print('Recall:', nltk.metrics.recall(reference_set['calm'], test_set['calm']))
            
            print('/----------------- ENERGETIC -----------------/')
            print('Precision:', nltk.metrics.precision(reference_set['energetic'], test_set['energetic']))
            print('Recall:', nltk.metrics.recall(reference_set['energetic'], test_set['energetic']))

            return {}
        
        elif self.execute is 'json':

            data = {
                    'accuracy': nltk.classify.util.accuracy(classifier, data_dict['test']),
                     'sentiment': {'sad': {'precision': nltk.metrics.precision(reference_set['sad'], test_set['sad']), 'recall': nltk.metrics.recall(reference_set['sad'], test_set['sad'])},
                        'calm': {'precision': nltk.metrics.precision(reference_set['calm'], test_set['calm']), 'recall': nltk.metrics.recall(reference_set['calm'], test_set['calm'])},
                        'energetic': {'precision': nltk.metrics.precision(reference_set['energetic'], test_set['energetic']), 'recall': nltk.metrics.recall(reference_set['energetic'], test_set['energetic'])}
                        }
                    }

            return data
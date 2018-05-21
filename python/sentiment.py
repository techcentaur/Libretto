import re
import os
import math
import argparse
import itertools
import collections
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
from nltk.metrics.scores import precision, recall

class Sentiment:
    def __init__(self, quiet):
        self.folder_name = '../dataset'
        self.quiet = quiet

    def feature_dict(self, words):
        return dict([(word, True) for word in words])

    def create_sets(self, featuredict):

        categories_dict = {'sad': {'features':[], 'datapath': os.path.join(self.folder_name, 'sad'), 'cutoff': 0.0},
                        'calm': {'features':[], 'datapath': os.path.join(self.folder_name, 'calm'), 'cutoff': 0.0},
                        'energetic': {'features':[], 'datapath': os.path.join(self.folder_name, 'energetic'), 'cutoff': 0.0}}

        for key in categories_dict:
            with open(categories_dict[key]['datapath']+".txt", 'r') as datalist:
                for data in datalist:
                    words = re.findall(r"[\w']+ | [.,!?;]", data.rstrip())
                    words = self.stopwords(" ".join(words))
                    words = [featuredict(words), key]
                    categories_dict[key]['features'].append(words)

        for key in categories_dict:
            categories_dict[key]['cutoff'] = int(math.floor(len(categories_dict[key]['features']) * 0.75))

        train_features = []
        test_features = []

        for key in categories_dict:
            for feature in ((categories_dict[key]['features'])[:(categories_dict[key]['cutoff'])]):
                train_features.append(feature) 
            for feature in ((categories_dict[key]['features'])[(categories_dict[key]['cutoff']):]):
                test_features.append(feature) 
        
        return {'train': train_features, 'test': test_features}

    
    def machine_model(self, data_dict):

        classifier = NaiveBayesClassifier.train(data_dict['train'])

        reference_set = collections.defaultdict(set)
        test_set = collections.defaultdict(set)

        for i, (features, key) in enumerate(data_dict['test']):
            reference_set[key].add(i)

            predict = classifier.classify(features)
            test_set[predict].add(i)

        if not self.quiet:
            
            print('[*] Trained on {trainf} instances and tested on {testf} instances ...'.format(trainf=len(data_dict['train']), testf=len(data_dict['test'])))
            print('\n[*] Accuracy:', nltk.classify.util.accuracy(classifier, data_dict['test']), end='\n')
            
            print('\n/------------------- SAD ------------------/')
            print('[.] Precision:', precision(reference_set['sad'], test_set['sad']))
            print('[.] Recall:', recall(reference_set['sad'], test_set['sad']))
            
            print('\n/------------------- CALM -------------------/')
            print('[.] Precision:', precision(reference_set['calm'], test_set['calm']))
            print('[.] Recall:', recall(reference_set['calm'], test_set['calm']))
            
            print('\n/----------------- ENERGETIC -----------------/')
            print('[.] Precision:', precision(reference_set['energetic'], test_set['energetic']))
            print('[.] Recall:', recall(reference_set['energetic'], test_set['energetic']))

            return {}
        
        else:
            data = {
                    'accuracy': nltk.classify.util.accuracy(classifier, data_dict['test']),
                     'sentiment': {'sad': {'precision': nltk.metrics.precision(reference_set['sad'], test_set['sad']), 'recall': nltk.metrics.recall(reference_set['sad'], test_set['sad'])},
                        'calm': {'precision': nltk.metrics.precision(reference_set['calm'], test_set['calm']), 'recall': nltk.metrics.recall(reference_set['calm'], test_set['calm'])},
                        'energetic': {'precision': nltk.metrics.precision(reference_set['energetic'], test_set['energetic']), 'recall': nltk.metrics.recall(reference_set['energetic'], test_set['energetic'])}
                        }
                    }

            return data

    def stopwords(self, text):
        stop_words = set(stopwords.words('english'))

        porter = PorterStemmer()
        # with stemming
        # tokens = [porter.stem(i.lower()) for i in wordpunct_tokenize(text) if i.lower() not in stop_words]
        # without stemming
        tokens = [i.lower() for i in wordpunct_tokenize(text) if i.lower() not in stop_words]

        return tokens


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Sentiment Analysis in categories as sad, calm and energetic')
    
    parser.add_argument('-q', "--quiet", help="quieter analysing", action='store_true', default = False)
    args = parser.parse_args()

    sent = Sentiment(args.quiet)
    data_dict = sent.machine_model(sent.create_sets(sent.feature_dict))

    if args.quiet:
        with open('analysis.json', 'w') as outfile:
            json.dump(data_dict, outfile, indent=4)          


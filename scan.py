import nltk
import argparse
import nltk.corpus
import operator
from string import punctuation
from collections import defaultdict

class Scan:

	def __init__(self, string):
		self.text = string
	
	
	def frequency_dict(self, reject_extreme_values=True):
		self.freq_dict = defaultdict(float)
		
		for line in self.text_tokens:
			for w in line:
				if w not in set(nltk.corpus.stopwords.words('english')+list(punctuation)):
					self.freq_dict[w]+=1

		if reject_extreme_values:
			maximum = float(max(self.freq_dict.values()))
			
			for (w, v) in self.freq_dict.items():
				self.freq_dict[w] = v / maximum
				if self.freq_dict[w] >= 0.85 or self.freq_dict[w] <= 0.15:
					self.freq_dict[w] = v - 1 


	def sentence_rank(self, num):
		summary_lines=[]
		sentence_rank = defaultdict(float)
		
		for sentence in self.text_tokens:
			s = " ".join(sentence)

			for word in sentence:
				if word in self.freq_dict:
					sentence_rank[s] += self.freq_dict[word]
		
		for (w,v) in sentence_rank.items():
			sentence_rank[w] = v / len(w)

		for i in range(0, num):
			if len(sentence_rank)!=0:
				s = max( sentence_rank.items(), key = operator.itemgetter(1))[0]	
				summary_lines.append(s)

				del sentence_rank[s]

		return summary_lines


	def calculate_summary(self, num):
		sentence_tokens = nltk.sent_tokenize(self.text)
		
		self.text_tokens=[]
		for tok in sentence_tokens:
			self.text_tokens.append( nltk.word_tokenize(tok.lower()) ) 

		self.frequency_dict()
		summary = self.sentence_rank(num)

		return summary	

import re, argparse, nltk
from lyrics import Scraper
from scan import Scan
from string import punctuation
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

class Clean:
	def __init__(self, tokens):
		self.tokens = tokens
		for i in range(0, len(self.tokens)):
			self.tokens[i] = self.tokens[i].lower()

	def idiosyncracies_remove(self):
		raw = " ".join(self.tokens)

		raw = raw.replace('[','<')
		raw = raw.replace(']','>')
		raw = re.sub('<[^>]+>','',raw)

		self.tokens = nltk.word_tokenize(raw)
		return self.tokens

	def apostrophe_normalisation(self):
		
		text = " ".join(self.tokens)
		text = re.sub(r"n\'t", " not", text)
		text = re.sub(r"\'re", " are", text)
		text = re.sub(r"\'s", " is", text)
		text = re.sub(r"\'d", " would", text)
		text = re.sub(r"\'ll", " will", text)
		text = re.sub(r"\'t", " not", text)
		text = re.sub(r"\'ve", " have", text)
		text = re.sub(r"\'m", " am", text)

		self.tokens = nltk.word_tokenize(text)
		return self.tokens

	def normalize(self):
		lem = WordNetLemmatizer()
		clean_tokens = self.tokens

		for (w,t) in pos_tag(clean_tokens):
			wt = t[0].lower()
			
			wt = [wt if wt in ['a','r','n','v'] else None]
			
			wnew = lem.lemmatize(w,wt) if wt else None
			clean_tokens.remove(w)
			clean_tokens.append(wnew)

		self.tokens = clean_tokens
		return clean_tokens

	def stopwords_remove(self):		
		toks = self.tokens
		stopwords = set(stopwords.words('english'))

		clean_tokens = [x for x in toks if not x in stopwords]
		self.tokens = clean_tokens
		return clean_tokens


	def punctuation_remove(self):
		clean_tokens = self.tokens
		punc_list = list(punctuation)

		for i in clean_tokens:
			if i in punc_list:
				clean_tokens.remove(i)
		
		self.tokens = clean_tokens
		return clean_tokens


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Libretto: Analyse songs you like, get results you dont')
	
	parser.add_argument('-s', "--song", help="song name", type=str)
	parser.add_argument('-S', "--singer", help="singer name", type=str)
	args = parser.parse_args()

	scraper = Scraper(args.song, args.singer)
	lyrics = scraper.get_lyrics()

	text = lyrics[0]
	text = text.replace("\n",". ")
	text = text.replace("\t","")
	text = text.replace("\r","")

	text_list = text.split(" ")
	for i in range(0, len(text_list)):
		if text_list[i].endswith('.'):
			text_list[i] = text_list[i][:-1]
	for i in range(0, len(text_list)):
		if text_list[i].endswith('?'):
			text_list[i] = text_list[i][:-1]

	text_list = list(filter(None, text_list)) 

	clean = Clean(text_list)

	clean.punctuation_remove()
	clean.apostrophe_normalisation()
	clean.idiosyncracies_remove()

	string = ". ".join(clean.tokens)
	file = open('testing.txt', 'w')

	file.write(string)
	file.close()

	s = Scan("testing.txt")
	sl = s.calculate_summary(int(input("[*] How much lines..."))) 

	print(sl)
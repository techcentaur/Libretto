import re, argparse, nltk, googletrans
from lyrics import Scraper
from string import punctuation
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

class Libretto:
	def __init__(self, text):
		self.text = text
		# self.tokens = nltk.word_tokenize(text)
		# for i in range(0, len(self.tokens)):
		# 	self.tokens[i] = self.tokens[i].lower()

	def idiosyncracies_remove(self):
		raw = self.text

		raw = raw.replace('[','<')
		raw = raw.replace(']','>')
		raw = re.sub('<[^>]+>','',raw)

		return raw

	def apostrophe_normalisation(self):
		
		raw = self.text
		raw = re.sub(r"n\'t", " not", raw)
		raw = re.sub(r"\'re", " are", raw)
		raw = re.sub(r"\'s", " is", raw)
		raw = re.sub(r"\'d", " would", raw)
		raw = re.sub(r"\'ll", " will", raw)
		raw = re.sub(r"\'t", " not", raw)
		raw = re.sub(r"\'ve", " have", raw)
		raw = re.sub(r"\'m", " am", raw)
		raw = re.sub(r"\'cause", "because", raw)
		raw = re.sub(r"\'Cause", "Because", raw)

		return raw

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


	def langauage_detection(self):
		translator = googletrans.Translator()
		l = translator.detect(self.text)

		return [l.lang, l.confidence]

	def para_to_string(self):
		raw = self.text

		raw = raw.replace('\n\n\n', '. ')
		raw = raw.replace('\n\n', '. ')
		raw = raw.replace('\n', '. ')

		return raw

	def cleanse_lyrics(self):
		raw = self.text

		raw = self.idiosyncracies_remove()
		self.text = raw

		raw = self.apostrophe_normalisation()
		self.text = raw
		
		raw = self.para_to_string()
		self.text = raw
		return raw



if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Libretto: Analyse songs you like, get results you don\'t.')
	
	parser.add_argument('-s', "--song", help="song name", type=str)
	parser.add_argument('-S', "--singer", help="singer name", type=str)
	parser.add_argument('-q', "--quiet", help="quieter analysing", action='store_true')
	args = parser.parse_args()

	scraper = Scraper(args.song, args.singer)
	lyrics = scraper.get_lyrics()

	lib = Libretto(lyrics[0])
	lib.cleanse_lyrics()

	lang = lib.langauage_detection()

	if not args.quiet:
		print("[*] Language:", lang[0],"[confidence:", str(lang[1]), "%]")
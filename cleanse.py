import argparse, nltk
from lyrics import Scraper
from string import punctuation
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

class Clean:
	def __init__(self, tokens):
		self.tokens = tokens
		for i in range(0, len(self.tokens)):
			self.tokens[i] = self.tokens[i].lower()

	def apostrophe_normalisation(self):
		text = " ".join(words)
		text = re.sub(r"n\'t", " not", text)
		text = re.sub(r"\'re", " are", text)
		text = re.sub(r"\'s", " is", text)
		text = re.sub(r"\'d", " would", text)
		text = re.sub(r"\'ll", " will", text)
		text = re.sub(r"\'t", " not", text)
		text = re.sub(r"\'ve", " have", text)
		text = re.sub(r"\'m", " am", text)

		w = ntlk.word_tokenize(text)
		return w


	def stopwords_remove(self):		
		toks = self.tokens
		stopwords = set(stopwords.words('english'))

		clean_tokens = [x for x in toks if not x in stopwords]
		return clean_tokens


	def punctuation_remove(self):
		clean_tokens = self.tokens
		punc_list = list(punctuation)

		for i in clean_tokens:
			if i in punc_list:
				clean_tokens.remove(i)
		
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

	l = clean.punctuation_remove()
	print(l)

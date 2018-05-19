import re, argparse, nltk, googletrans
from lyrics import Scraper
from string import punctuation
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from scan import Scan

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

	def cleanse_lyrics(self, quiet):
		raw = self.text

		if not quiet:
			print('[!] Idiosyncracies removed like [Chorus]: [Verse]: ...')
		raw = self.idiosyncracies_remove()
		self.text = raw

		if not quiet:
			print('[!] Normalising words - apostrophe removal ...')
		raw = self.apostrophe_normalisation()
		self.text = raw
		
		if not quiet:
			print('[!] Creating lyrical-verses to string ...')
		raw = self.para_to_string()
		self.text = raw
		return raw

	def NER(self):
		raw = self.text
		ner = []

		for sent in nltk.sent_tokenize(raw):
			for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
				if hasattr(chunk, 'label'):
					ner.append((chunk.label(), ' '.join(c[0] for c in chunk)))

		entityrecognition = {'FACILITY':[], 'GPE':[], 'GSP':[], 'LOCATION':[], 'ORGANIZATION':[], 'PERSON':[] }

		for i in ner:			
			entityrecognition[(i[0])].append(i[1])

		return entityrecognition

	def summarise(self):
		scanobj = Scan(self.text)

		summarylist = scanobj.calculate_summary(5)

		return summarylist

	def write_infile(self):
		file = open('song_data.txt', 'w')

		file.write(self.text)
		file.close()

		return True


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Libretto: Analyse songs you like, get results you don\'t.')
	
	parser.add_argument('-s', "--song", help="song name", type=str)
	parser.add_argument('-S', "--singer", help="singer name", type=str)
	parser.add_argument('-q', "--quiet", help="quieter analysing", action='store_true')
	args = parser.parse_args()

	if not args.quiet:
		print('[*] Scraping the lyrics of', args.song,'...\n')

	scraper = Scraper(args.song, args.singer)
	lyrics = scraper.get_lyrics()

	scraper.write_infile(lyrics)

	lib = Libretto(lyrics[0])
	lib.cleanse_lyrics(args.quiet)

	if not args.quiet:
		print('[!] Detecting language ...')

	lang = lib.langauage_detection()

	if not args.quiet:
		print("\n[*] Language:", lang[0],"[confidence:", str(lang[1]), "%]\n")

	if not args.quiet:
		print('[!] Named entity recognition on lyrics ...')

	entitydict = lib.NER()

	if not args.quiet:
		print('\n[*] Printing NER: ', entitydict,'\n')

	if not args.quiet:
		print('[!] Summarising song ...')

	summ = lib.summarise()
	if not args.quiet:
		print('\n[*] Summary of the song:')
		for i in range(0, len(summ)):
			print(str(i) + ". ", summ[i])

	lib.write_infile()
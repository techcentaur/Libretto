import re
import json
import nltk
import argparse
import googletrans

from string import punctuation
from python import scan, lyrics

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

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
		rawtext = self.text
		
		tokens = nltk.word_tokenize(tokens)
		stopwords = set(stopwords.words('english'))

		clean_tokens = [x for x in toks if not x in stopwords]
		tokens = " ".join(clean_tokens)
		return text


	def punctuation_remove(self):
		clean_tokens = (self.text).split(" ")
		punc_list = list(punctuation)

		for i in clean_tokens:
			if i in punc_list:
				clean_tokens.remove(i)
		
		text = " ".join(clean_tokens)
		return text


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
		scanobj = scan.Scan(self.text)

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
	parser.add_argument('-l', '--list', default='terminal', choices=['terminal', 'json'], help='terminal: stdout; json: save in JSON format')	
	args = parser.parse_args()

	if args.list == 'json':
		args.quiet = True
		is_json = True
	else:
		is_json = False

	if not args.quiet:
		print('[!] Scraping the lyrics of', args.song, 'by', args.singer, '...\n')

	lib_dict = {}

	scraper = lyrics.Scraper(args.song, args.singer)
	lyrics = scraper.get_lyrics()

	scraper.write_infile(lyrics)

	lib = Libretto(lyrics[0])
	lib.cleanse_lyrics(args.quiet)

	if not args.quiet:
		print('[!] Detecting language ...')

	lang = lib.langauage_detection()
	
	if not is_json:
		print("\n[*] Language:", lang[0],"[confidence:", str(lang[1]), "%]\n")
	else:
		lib_dict['language'] = {'language': lang[0], 'confidence': lang[1]}

	if not args.quiet:
		print('[!] Named entity recognition on lyrics ...\n')

	entitydict = lib.NER()

	if not is_json:
		print('[*] Named Entity Recognition: ', entitydict,'\n')
	else:
		lib_dict['NER'] = entitydict

	if not args.quiet:
		print('[!] Summarising song ...')

	summ = lib.summarise()
	if not is_json:
		print('\n[*] Summary of', args.song, ':')
		for i in range(0, len(summ)):
			print(str(i) + ". ", summ[i])
	else:
		lib_dict['summary'] = summ

	lib.write_infile()

	if is_json:
		with open("_" + args.song + "_libretto.json", 'w') as outfile:
			json.dump(lib_dict, outfile, indent=4)			

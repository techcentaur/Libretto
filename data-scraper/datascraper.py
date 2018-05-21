import sys
import argparse
sys.path.append('/home/gavy42/Desktop/github/Libretto/python')
sys.path.append('/home/gavy42/Desktop/github/Libretto')
from lyrics import Scraper
from app import Libretto

class Scrapedata(object):
    """Scraping the lyrical dataset"""
    def __init__(self, quiet = False):
        self.quiet = quiet

    def scrape(self, filename, outfilename):

        if not self.quiet:
            print('[*] Reading song list from', filename,'...')

        try:
            with open(filename, 'r') as songsfile:
                songs = songsfile.read()
        except FileNotFoundError:
            print('[-_-!] File not found ... :(')

        list1 = songs.split('\n\n')
        list2 = []

        for l in list1:
            list2 .append(l.split('\n'))

        if not self.quiet:
            print('[*] Read', len(list2), 'song details ...\n')
            print('[**] Scraping phase initiated ...\n')

        lyrics_data = ""

        for i in list2:
            try:
                lyrics = Scraper(i[0], i[1]).get_lyrics()
                lyrics_data += lyrics[0]

                if not self.quiet:
                    print('[**] Lyrics scraped of', i[0],'by', i[1], '...')
            except Exception:
                pass

        clean_lyrics_data = Libretto(lyrics_data).cleanse_lyrics(True)

        if not self.quiet:
            print('\n[***] Writing data in', outfilename, '...')

        try:
            with open(outfilename, 'w') as datafile:
                datafile.write(clean_lyrics_data)
        except FileNotFoundError:
            print('[-_-!] File not found ... :(')

        datafile.close()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description = 'Scrape lyrics reading songs from a file')

    parser.add_argument('-i', '--input', help='Input file containing song\'s name', default = 'songs.txt')
    parser.add_argument('-o', '--output', help='Output file in which data will be retrieved', default = 'data_lyrics_songs.txt')
    parser.add_argument('-q', '--quiet', help='Do quiet processing', default= False, action="store_true")
    
    args = parser.parse_args()

    Scrapedata(args.quiet).scrape(args.input, args.output)

    if not args.quiet:
        print('\n[***] Scraping done.')
        print('/------------------------- Made by: Techcentaur -------------------/')
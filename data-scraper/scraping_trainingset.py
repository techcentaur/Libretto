import sys
import argparse
sys.path.append('/home/gavy42/Desktop/github/Libretto/python')
sys.path.append('/home/gavy42/Desktop/github/Libretto')
from lyrics import Scraper
from app import Libretto

class Scrapedata(object):
    """Scraping the lyrical dataset"""
    def __init__(self):
        pass

    def scrape(self, filename, outfilename):

        with open(filename, 'r') as songsfile:
            songs = songsfile.read()

        list1 = songs.split('\n\n')
        list2 = []

        for l in list1:
            list2 .append(l.split('\n'))

        lyrics_data = ""

        for i in list2:
            lyrics = Scraper(i[0], i[1]).get_lyrics()

            lyrics_data += lyrics[0]


        clean_lyrics_data = Libretto(lyrics_data).cleanse_lyrics(True)

        with open(outfilename, 'w') as datafile:
            datafile.write(clean_lyrics_data)

        datafile.close()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description = 'Scrape lyrics reading songs from a file')

    parser.add_argument('-i', '--input', help='input file containing song\'s name', default = 'songs.txt')
    parser.add_argument('-o', '--output', help='output file in which data will be retrieved', default = 'data_lyrics_songs.txt')
    
    args = parser.parse_args()

    Scrapedata().scrape(args.input, args.output)
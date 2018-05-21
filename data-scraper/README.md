## DataScraping

Scrape data (lyrics of songs) online, reading from a file.

## Usage

#### Argparse usage
```console
gavy42@jarvis:~/Libretto/data-scraper$ python3 datascraper.py -h
usage: datascraper.py [-h] [-i INPUT] [-o OUTPUT] [-q]

Scrape lyrics reading songs from a file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file containing song's name
  -o OUTPUT, --output OUTPUT
                        Output file in which data will be retrieved
  -q, --quiet           Do quiet processing
```

#### Functions usage

- Create an instance of class as `Scrapedata(<quiet>)`, where quiet is optional argparse argument, to process quiet; it is by default `False`.

- Use function `scrape(self, filename, outfilename)` to get scraped content in `outfilename`, where songs are written in a file as `filename`.

## File format

- `filename` as input, should be a text file in this format.
```text
songname1
singername1

songname2
singername2

songname3
singername3

...
```

### Note

- Made to scrape lyrics, to create dataset with different themes, for the sentiment analysis using Navie's Baye classifier.

### Support

- If you've any trouble related to the code, let's discuss it. Feel free to create an issue! or contribute on the other side.

- Feel free to hit me up; [Techcentaur](https://www.github.com/techcentaur).


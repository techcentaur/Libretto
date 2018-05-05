# Libretto
Analyse songs you like, get results you don't. Works through NLP.

## Usage

#### Help Usage

```console
gavy42@jarvis:~/Desktop/github/Libretto$ python3 cleanse.py -h
usage: cleanse.py [-h] [-s SONG] [-S SINGER]

Libretto: Analyse songs you like, get results you dont

optional arguments:
  -h, --help            show this help message and exit
  -s SONG, --song SONG  song name
  -S SINGER, --singer SINGER
                        singer name
```

#### Interpreter Usage
```python3
>>> from cleanse import Clean
>>> c = Clean(['ankit', 'solanki'])
>>> c
<cleanse.Clean object at 0x7f1de940dda0>
```

#### Functional Usage

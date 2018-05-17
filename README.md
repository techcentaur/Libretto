# Libretto
Analyse songs you like, get results you don't. Works through NLP.

## Implementation Aims

- Language guessing of lyrics and title - **CHECK**
- Structure extraction; get verses and choruses (chorus: repeating words)
- Name, entity and place recognition used in lyrics - **CHECK**
- Theme categorization (e.g. happy | sad)
- Figure of speech detection (certain FoS's)

## Usage

#### Help Usage

```console
gavy42@jarvis:~/Desktop/github/Libretto$ python3 app.py -h
usage: app.py [-h] [-s SONG] [-S SINGER]

Libretto: Analyse songs you like, get results you don't.

optional arguments:
  -h, --help            show this help message and exit
  -s SONG, --song SONG  song name
  -S SINGER, --singer SINGER
                        singer name
```

#### Interpreter Usage

```python3
>>> from app import Libretto
>>> lib = Libretto(['ankit', 'solanki'])
>>> lib
<app.Libretto object at 0x7f1de940dda0>
```

#### Functional Usage

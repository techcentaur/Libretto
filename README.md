# Libretto
Analyse songs you like, get results you don't. Works through NLP.

## Usage

#### Help Usage
```console
gavy42@jarvis:~/Libretto$ python3 app.py -h
usage: app.py [-h] [-s SONG] [-S SINGER] [-q] [-l {terminal,json}]

Libretto: Analyse songs you like, get results you don't.

optional arguments:
  -h, --help            show this help message and exit
  -s SONG, --song SONG  song name
  -S SINGER, --singer SINGER
                        singer name
  -q, --quiet           quieter analysing
  -l {terminal,json}, --list {terminal,json}
                        terminal: stdout; json: save in JSON format
```

#### Interpreter Usage

```python3
>>> from app import Libretto
>>> lib = Libretto("this is a sample text, I like navyblue.")
>>> lib
<app.Libretto object at 0x7f1de940dda0>
```

#### Functional Usage

After creating the instance of the class Libretto as `Libretto(<text_string>)`; these functions are available as public to utilise.

- `cleanse_lyrics(<args.quiet>)` : Returns clean lyrics
  - `idiosyncracies_remove()`
  - `apostrophe_normalisation()`

## JSON format datafile

```json
{
    "language": {
        "language": "",
        "confidence":
    },
    "NER": {
        "FACILITY": [],
        "GPE": [],
        "GSP": [],
        "LOCATION": [],
        "ORGANIZATION": [],
        "PERSON": []
    },
    "summary": []
}
```

## Implementation Aims Remaining

- Theme categorization using machine learning (language processing)
- Genre classification using deep learning (audio analysis)
- Structure extraction; get verses and choruses (chorus: repeating words)
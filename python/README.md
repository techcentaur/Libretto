# Sentiment Analysis


## Usage

#### Argparse usage

```console
gavy42@jarvis:~/Libretto/python$ python3 sentiment.py -husage: sentiment.py [-h] [-q]

Sentiment Analysis in categories as sad, calm and energetic

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  quieter analysing
```

#### Function usage

- Create an instance of class as `Sentiment(<quiet>)`, where quiet is optional argparse argument, to process quiet; it is by default `False`.

- `create_sets(featuredict)`: Returns a dict containing a structure as `{'train': train_features, 'test': test_features}`, where names have their usual meaning.

- `machine_model(data_dict)`: Returns a dict, in case `quiet = True`, it will return a dict with precisions, recalls, and accuracy; otherwise it will print out the same.


## JSON format
```json
{
    "accuracy": 0.5595238095238095,
    "sentiment": {
        "sad": {
            "precision": 0.5625,
            "recall": 0.8571428571428571
        },
        "calm": {
            "precision": 0.4,
            "recall": 0.14285714285714285
        },
        "energetic": {
            "precision": 0.7,
            "recall": 0.5
        }
    }
}
```

### Support

- If you've any trouble related to the code, let's discuss it. Feel free to create an issue! or contribute on the other side.

- Feel free to hit me up; [Techcentaur](https://www.github.com/techcentaur).


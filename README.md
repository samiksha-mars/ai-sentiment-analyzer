# AI Sentiment Analyzer

A lightweight, rule-based sentiment analyzer that labels text as **positive**,
**negative** or **neutral**. Inspired by lexicon approaches such as VADER and
built with only the Python standard library.

## Features

- Word-level sentiment lexicon (`lexicon.json`) you can extend
- Handles negation ("not good" is negative)
- Handles intensifiers and dampeners ("very good", "slightly bad")
- Boosts scores for exclamation marks
- Analyze a single sentence, a file, or stdin, line by line

## Usage

```bash
python3 sentiment.py "This is very good"
# positive  +3.00  This is very good

# Analyze every line of a file
python3 sentiment.py -f examples.txt
# positive  +6.30  I love this phone, the camera is amazing!
# negative  -4.00  The delivery was not good and support was rude.
# neutral   +0.00  It arrived on Tuesday.
# negative  -1.25  The battery is slightly disappointing.

# Read from stdin
echo "What a terrible movie" | python3 sentiment.py

# Use your own lexicon
python3 sentiment.py "..." --lexicon my_lexicon.json
```

Scores of `+0.5` or more are positive, `-0.5` or less are negative, anything in
between is neutral.

## Tests

```bash
python3 -m unittest test_sentiment.py
```

"""Rule-based sentiment analyzer with negation and intensifier handling."""

import json
import re
from pathlib import Path

DEFAULT_LEXICON = Path(__file__).with_name("lexicon.json")

NEGATIONS = {"not", "no", "never", "none", "nobody", "nothing", "neither", "nor",
             "cannot", "cant", "dont", "doesnt", "didnt", "isnt", "wasnt", "arent",
             "wont", "wouldnt", "shouldnt", "couldnt", "aint", "hardly"}
MODIFIERS = {"very": 1.5, "really": 1.4, "extremely": 1.8, "so": 1.3, "super": 1.5,
             "incredibly": 1.8, "absolutely": 1.6, "totally": 1.4, "quite": 1.2,
             "slightly": 0.5, "somewhat": 0.7, "barely": 0.4, "kinda": 0.7}
NEGATION_WINDOW = 3
EXCLAMATION_BOOST = 0.3
THRESHOLD = 0.5

TOKEN_RE = re.compile(r"[a-z']+")


def tokenize(text):
    """Lowercase words with apostrophes removed ("don't" -> "dont")."""
    return [t.replace("'", "") for t in TOKEN_RE.findall(text.lower())]


def load_lexicon(path=DEFAULT_LEXICON):
    with open(path, encoding="utf-8") as f:
        return {word.lower(): float(score) for word, score in json.loads(f.read()).items()}


class SentimentAnalyzer:

    def __init__(self, lexicon=None):
        self.lexicon = lexicon if lexicon is not None else load_lexicon()

    def score(self, text):
        """Return the raw sentiment score of the text (positive > 0 > negative)."""
        tokens = tokenize(text)
        total = 0.0
        for i, token in enumerate(tokens):
            value = self.lexicon.get(token)
            if value is None:
                continue
            if i > 0 and tokens[i - 1] in MODIFIERS:
                value *= MODIFIERS[tokens[i - 1]]
            window = tokens[max(0, i - NEGATION_WINDOW):i]
            if any(word in NEGATIONS for word in window):
                value *= -0.75
            total += value

        exclamations = min(text.count("!"), 3)
        if total > 0:
            total += exclamations * EXCLAMATION_BOOST
        elif total < 0:
            total -= exclamations * EXCLAMATION_BOOST
        return round(total, 3)

    def label(self, text):
        """Return 'positive', 'negative' or 'neutral'."""
        return label_for(self.score(text))

    def analyze(self, text):
        value = self.score(text)
        return {"text": text, "score": value, "label": label_for(value)}


def label_for(value):
    if value >= THRESHOLD:
        return "positive"
    if value <= -THRESHOLD:
        return "negative"
    return "neutral"

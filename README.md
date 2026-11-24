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

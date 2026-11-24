import unittest

from sentiment import SentimentAnalyzer, tokenize

LEXICON = {"good": 2.0, "bad": -2.0, "love": 3.0}


class TokenizeTest(unittest.TestCase):

    def test_strips_apostrophes(self):
        self.assertEqual(tokenize("Don't stop!"), ["dont", "stop"])


class SentimentAnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.analyzer = SentimentAnalyzer(LEXICON)

    def test_positive(self):
        self.assertEqual(self.analyzer.label("This is good"), "positive")

    def test_negative(self):
        self.assertEqual(self.analyzer.label("This is bad"), "negative")

    def test_neutral_when_no_known_words(self):
        self.assertEqual(self.analyzer.label("The sky is blue"), "neutral")
        self.assertEqual(self.analyzer.score("The sky is blue"), 0)

    def test_negation_flips_sentiment(self):
        self.assertEqual(self.analyzer.label("This is not good"), "negative")
        self.assertEqual(self.analyzer.label("It isn't bad"), "positive")

    def test_intensifier_increases_score(self):
        self.assertGreater(self.analyzer.score("very good"), self.analyzer.score("good"))

    def test_dampener_decreases_score(self):
        self.assertLess(self.analyzer.score("slightly good"), self.analyzer.score("good"))

    def test_exclamation_boost(self):
        self.assertGreater(self.analyzer.score("good!!"), self.analyzer.score("good"))
        self.assertLess(self.analyzer.score("bad!!"), self.analyzer.score("bad"))

    def test_analyze_returns_all_fields(self):
        result = self.analyzer.analyze("I love it")
        self.assertEqual(result, {"text": "I love it", "score": 3.0, "label": "positive"})

    def test_default_lexicon_loads(self):
        self.assertEqual(SentimentAnalyzer().label("What an amazing day"), "positive")


if __name__ == "__main__":
    unittest.main()

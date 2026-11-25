import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from sentiment import SentimentAnalyzer, load_lexicon, main, tokenize

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


class LoadLexiconTest(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def write(self, content):
        path = self.dir / "lexicon.json"
        path.write_text(content, encoding="utf-8")
        return path

    def test_lowercases_words(self):
        self.assertEqual(load_lexicon(self.write('{"Good": 2}')), {"good": 2.0})

    def test_invalid_lexicons_raise_value_error(self):
        for content in ("not json", '["good"]', '{"good": "yes"}'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                load_lexicon(self.write(content))


class CliTest(unittest.TestCase):

    def run_main(self, argv):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_scores_text_argument(self):
        code, out, _ = self.run_main(["This is very good"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "positive  +3.00  This is very good\n")

    def test_missing_file_is_reported(self):
        code, out, err = self.run_main(["-f", "does-not-exist.txt"])
        self.assertEqual(code, 1)
        self.assertIn("Error:", err)

    def test_bad_lexicon_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            lexicon = Path(tmp, "bad.json")
            lexicon.write_text("[]", encoding="utf-8")
            code, _, err = self.run_main(["good", "--lexicon", str(lexicon)])
        self.assertEqual(code, 1)
        self.assertIn("JSON object", err)


if __name__ == "__main__":
    unittest.main()

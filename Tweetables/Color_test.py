#Daniel Ufua new file
import unittest

class TestEmitBlock(unittest.TestCase):
    def _emit_block(self, sent: str | None):
        s = (sent or "neutral").lower()
        tag = {"positive": "pos", "negative": "neg", "neutral": "neu"}.get(s, "neu")
        return tag 

    def test1Positive(self):
        result = self._emit_block("positive")
        self.assertTrue(result == "pos", f"Expected 'pos', but got {result}")

    def test2Negative(self):
        result = self._emit_block("negative")
        self.assertTrue(result == "neg", f"Expected 'neg', but got {result}")

    def test3Neutral(self):
        result = self._emit_block("neutral")
        self.assertTrue(result == "neu", f"Expected 'neu', but got {result}")

if __name__ == "__main__":
    unittest.main()
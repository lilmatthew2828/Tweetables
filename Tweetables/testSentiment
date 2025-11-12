#This file uses the unittest framework to verify that words within the dictionary
# are classified correctly

import unittest
from analyze_sentiment import analyze_sentiment, sentiment_dict



class TestSentiment(unittest.TestCase):
  # Test Sentiment method definition
  def test_dictionary(self):
    # Loops through each word within the dictionary as well as its assigned sentiment score
    for word ,score in sentiment_dict.items():
      # Runs the analyze sentiment function on each word that is iterated through the loop
      label, final_score = analyze_sentiment([word])
      # Determines the sentiment score based on a greater than or less than value
      if score > 0:
         expected = "positive"
      elif score < 0:
         expected = "negative"
      else:
         expected = "neutral"

      # Runs a test for each word that determines if/when a word fails

      with self.subTest(word=word):

          # Check if the label assigned matches what is expected
         self.assertEqual(label, expected, f"Expected {expected} for entity '{word}', instead got {label}")
          # Checks if the predicted score is equivalent to the score stored in the dictionary
         self.assertEqual(score, final_score, f"Word '{word}' score mismatch.")

if __name__ == "__main__":
    unittest.main()

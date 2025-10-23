# fetch_tweets.py  — portable outputs
import os
import sys
import re
import json
import shlex
import subprocess
from datetime import datetime
from neo4j import GraphDatabase
from twitter_setup import get_twitter_client
from langdetect import detect, LangDetectException

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg: str) -> None:
    print(msg, flush=True)

log("fetch_tweets.py has started running...")

# -------------------
# Helpers
# -------------------
def remove_emojis(tweet_text: str) -> str:
    """Remove non-ASCII characters (no emojis)."""
    return re.sub(r"[^\x00-\x7F]+", "", tweet_text)

def is_english(tweet_text: str) -> bool:
    """Return True if detected language is English."""
    try:
        return detect(tweet_text) == "en"
    except LangDetectException:
        return False


# ------------------------------
# Neo4j setup
# ------------------------------
import os
import sys
import re
import json
import shlex
import subprocess
from datetime import datetime
from neo4j import GraphDatabase
from twitter_setup import get_twitter_client
from langdetect import detect, LangDetectException

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg: str) -> None:
    print(msg, flush=True)

log("fetch_tweets.py has started running...")

# -------------------
# Helpers
# -------------------
def remove_emojis(tweet_text: str) -> str:
    """Quickly strip non-ASCII (good enough for demo emoji cleanup)."""
    return re.sub(r"[^\x00-\x7F]+", "", tweet_text)

def is_english(tweet_text: str) -> bool:
    """True if langdetect says 'en'; treat failures as non-English."""
    try:
        return detect(tweet_text) == "en"
    except LangDetectException:
        return False


# ------------------------------
# Neo4j setup
# ------------------------------
URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

def store_raw_tweets(records, keyword, username=None):
    """Store fetched tweets into Neo4j"""
    if not records:
        print("No tweet records to insert.")
        return

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        def insert_tweet(tx, tweet, keyword, username):
            query = """
                MERGE (t:Tweet {id: $id})
                ON CREATE SET
                    t.text = $text,
                    t.language = $language,
                    t.created_at = datetime()
                WITH t, $keyword AS kw
                MERGE (k:Keyword {name: kw})
                MERGE (t)-[:MENTIONS]->(k)
                WITH k, $username AS uname
                FOREACH (
                    i IN CASE WHEN uname IS NOT NULL THEN [1] ELSE [] END |
                    MERGE (u:USER {username: uname})
                    MERGE (u)-[:SEARCHED]->(k)
                )
            """
            tx.run(
                query,
                id=tweet.get("id"),
                text=tweet.get("text"),
                keyword=keyword,
                language=tweet.get("language", "en"),
                username=username
            )

        with driver.session() as session:
            for tweet in records:
                session.execute_write(insert_tweet, tweet, keyword, username)

        print(f"Inserted {len(records)} tweets into Neo4j successfully.")




# ------------------------------
# Twitter API Fetch
# ------------------------------
def fetch_tweets_twitter(keyword: str, username: str, want: int = 10):
    """Fetch recent tweets via Twitter API v2"""
    client = get_twitter_client(username)
    response = client.search_recent_tweets(query=keyword, max_results=min(want, 100))

    if not response or not response.data:
        return []

    seen = set()
    tweets = []

    for tweet in response.data:
        text = (getattr(tweet, "text", "") or "").strip()
        text = remove_emojis(text).replace("\n", " ")
        if not text or not is_english(text) or text in seen:
            continue
        seen.add(text)
        tweets.append({"id": getattr(tweet, "id", None), "text": text})
        if len(tweets) >= want:
            break

    return tweets


# ------------------------------
# Orchestrator
# ------------------------------
def main():
    if len(sys.argv) < 3:
        log("Usage: python fetch_tweets.py \"keyword\" \"username\" [--count N] [--scrape]")
        sys.exit(0)

    keyword = sys.argv[1]
    username = sys.argv[2]
    count = 10

    if "--count" in sys.argv:
        try:
            count = int(sys.argv[sys.argv.index("--count") + 1])
        except Exception:
            pass

    log(f"Fetching {count} tweets for '{keyword}'...")

    try:
        tweets = fetch_tweets_twitter(keyword, username, want=count)
        if tweets:
            store_raw_tweets(tweets, keyword, username)
            log(f"{len(tweets)} tweets fetched from API and stored in Neo4j.")
            return
        else:
            log("No tweets from API or rate limit reached.")
    except Exception as e:
        if "429" in str(e) or "Too Many Requests" in str(e):
            log("Twitter API rate limit hit. Log in with another account or wait until reset.")
        else:
            log(f"Error fetching tweets: {e}")




if __name__ == "__main__":
    main()

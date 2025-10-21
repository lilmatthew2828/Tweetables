# import tweepy
# import sys
# import re
# from twitter_setup import client
# import langdetect
# from langdetect import detect, LangDetectException 

# # The Code Orgininally has an Application Programming Inteface(API) cap which is getting is the damn way. 
# # Next there is no NLTK corpus 
# # lastly i need to stop it letting it cap at 429
# # I added this packages:
# import os 
# import sys
# import json
# import subprocess
# import shlex
# from datetime import datetime
# # Run fetch with fallback enabled
# # subprocess.run([sys.executable, "fetch_tweets.py", "python lang:en", "--scrape"])
# import tweepy
# from twitter_setup import client # <- v2 Tweepy Client
# from langdetect import detect, LangDetectException

# # -------------------------------------------------------------------
# # Output files (we write BOTH for compatibility with other scripts):
# # - raw_tweets.txt   : plain text, one tweet per line
# # - tweets.jsonl     : JSON Lines, one object per line: {"id": "...", "text": "..."}
# # -------------------------------------------------------------------
# OUTFILE_TXT = "raw_tweets.txt"
# OUTFILE = "tweets.jsonl"
# OUTFILE_TXT   = os.environ.get("OUTFILE_TXT", "raw_tweets.txt")
# OUTFILE_JSONL = os.environ.get("OUTFILE_JSONL", "tweets.jsonl")
# def log(msg):
#     print(msg, flush=True)


# log("fetch_tweets.py has started running...")

# def remove_emojis(tweet_text):
#     """
#     Strip non-ASCII characters (quick way to remove emojis and odd symbols).
#     If you need finer control later, swap this for a more precise emoji regex.
#     """
#     return re.sub(r'[^\x00-\x7F]+', '', tweet_text)

# def is_english(tweet_text : str) -> str:
#     """
#     Use langdetect to keep only English tweets.
#     Treat detection failures as 'not English' so we skip them safely.
#     """
#     try:
#         #detect language
#         return detect(tweet_text) == 'en'
#     except LangDetectException:
#         return False #if detection fails, consider it not english



# #------------------------------------  
# # Writers 
# #------------------------------------
# def write_txt(lines):
#     with open(OUTFILE_TXT, "w", encoding="utf-8") as f:
#         for line in lines:
#             f.write(line + "\n")
    
# def write_jsonl(records):
#     with open(OUTFILE_JSONL, "w", encoding="utf-8") as f:
#         for rec in records:
#             f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# # def fetch_tweets_v2(keyword, count=10):
# #     """ Fetch tweets based on a keyword and display them """
# #     try:
# #         count = max(1, min(count, 10))
# #         # Fetch tweets with the provided keyword
# #         response = client.search_recent_tweets(query=keyword, max_results=100)
        
# #         raw_tweets = []
# #         seen_tweets = set()
# #         shown = 0

# #         if response and response.data:
# #             print(f"\nFetched tweets for keyword: '{keyword}'\n")

# #             for tweet in response.data:
# #                 if shown >= count:
# #                     break

# #                 text = tweet.text.strip()
# #                 text = remove_emojis(text)

# #                 if not text or not is_english(text) or text in seen_tweets:
# #                     continue #skip if the tweet is not in english or duplicate
                
# #                 text_one_line = text.replace("\n", " ")
# #                 raw_tweets.append(text_one_line)
# #                 seen_tweets.add(text_one_line)
# #                 shown += 1

# #             if not raw_tweets:
# #                 print("No suitable English tweets found.")
# #                 return
                
# #                 # save the files open file
# #             with open("raw_tweets.txt", "w", encoding="utf-8") as file:
# #                 for tweet in raw_tweets:
# #                     file.write(tweet + "\n")

# #             # Print aligned and numbered output
# #             print("Tweets Fetched:\n")
# #             max_digits = len(str(len(raw_tweets)))
# #             for i, tweet in enumerate(raw_tweets, 1):
# #                 num_str = f"{i}".rjust(max_digits)
# #                 print(f"{num_str}. {tweet}")
# #             print("\nAll tweets saved to 'raw_tweets.txt'.\n")

# #         else:
# #             print("No tweets found.")
# #     except Exception as e:
# #         print(f"Error fetching tweets: {e}")
# # ------------------------------
# # Fallback via snscrape (no API)
# # ------------------------------
# def run_snscrape(query: str, limit: int = 100) -> bool:
#     """
#     Requires: pip install snscrape
#     Produces: tweets.jsonl (JSONL) with {"id","text"} per line.
#     """
#     # snscrape emits JSONL to stdout; we capture it to OUTFILE_JSONL
#     cmd = f"snscrape --jsonl --max-results {int(limit)} twitter-search \"{query}\""
#     log(f"Running snscrape: {cmd}")
#     try:
#         proc = subprocess.run(
#             shlex.split(cmd),
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#     except FileNotFoundError:
#         log("snscrape is not installed or not on PATH. Install with: pip install snscrape")
#         return False

#     if proc.returncode != 0:
#         log("snscrape failed:\n" + (proc.stderr or ""))
#         return False

#     # snscrape JSON is verbose; normalize and write our own compact JSONL
#     jsonl_records = []
#     txt_lines = []
#     for line in proc.stdout.splitlines():
#         try:
#             obj = json.loads(line)
#             text = (obj.get("rawContent") or "").strip()
#             text = remove_emojis(text).replace("\n", " ")
#             if not text or not is_english(text):
#                 continue
#             tweet_id = obj.get("id")
#             jsonl_records.append({"id": tweet_id, "text": text})
#             txt_lines.append(text)
#         except json.JSONDecodeError:
#             continue

#     if not jsonl_records:
#         log("snscrape returned no usable tweets.")
#         return False

#     write_jsonl(jsonl_records)
#     write_txt(txt_lines)
#     return True

# # ------------------------------
# # Twitter API (Tweepy v2 client)
# # ------------------------------
# def fetch_tweets_twitter(keyword: str, want: int = 10):
#     """
#     Fetch recent tweets using the Twitter API v2 client.
#     - Deduplicate, clean, filter to English
#     - Return both plain-text list and JSONL-ready list
#     """
#     want = max(1, min(want, 2))  # guard rails; API max_results per call is 100

#     response = client.search_recent_tweets(query=keyword, max_results=2)
#     if not response or not response.data:
#         return [], []

#     seen = set()
#     txt_lines = []
#     jsonl_records = []

#     for tweet in response.data:
#         if len(txt_lines) >= want:
#             break
#         text = (tweet.text or "").strip()
#         text = remove_emojis(text).replace("\n", " ")
#         if not text or not is_english(text) or text in seen:
#             continue
#         seen.add(text)
#         txt_lines.append(text)
#         jsonl_records.append({"id": getattr(tweet, "id", None), "text": text})

#     return txt_lines, jsonl_records


# # ------------------------------
# # Orchestrator
# # ------------------------------
# def main():
#     # CLI usage:
#     #   python fetch_tweets.py "your keywords" --count 25
#     # Optional fallback:
#     #   python fetch_tweets.py "your keywords" --scrape
#     # or set env var:
#     #   set USE_SNSCRAPE=1
#     #   set SCRAPE_LIMIT=200
#     #   set SCRAPE_QUERY="from:nytimes lang:en since:2025-09-01"
#     #
#     if len(sys.argv) < 2:
#         log("No keyword provided. Example: python fetch_tweets.py \"python lang:en\"")
#         sys.exit(0)

#     keyword = sys.argv[1]
#     count = 10
#     use_scrape_flag = False

#     # Parse optional flags
#     if "--count" in sys.argv:
#         try:
#             count = int(sys.argv[sys.argv.index("--count") + 1])
#         except Exception:
#             pass
#     if "--scrape" in sys.argv:
#         use_scrape_flag = True

#     log(f"Fetching tweets for sentiment analysis...")
#     log(f"2 we're here")
#     try:
#         log("Using Twitter API v2...")
#         txt_lines, jsonl_records = fetch_tweets_twitter(keyword, want=count)
#         if not txt_lines:
#             log("No suitable English tweets found via API.")
#         else:
#             write_txt(txt_lines)
#             write_jsonl(jsonl_records)
#             _digits = len(str(len(txt_lines)))
#             log("\nTweets Fetched:\n")
#             for i, line in enumerate(txt_lines, 1):
#                 log(f"{str(i).rjust(_digits)}. {line}")
#             log(f"\nSaved {len(txt_lines)} tweets to '{OUTFILE_TXT}' and '{OUTFILE_JSONL}'.")
#             return

#     except Exception as e:
#         emsg = str(e)
#         # Handle rate limit or monthly cap as non-fatal
#         if "429" in emsg or "Too Many Requests" in emsg or "cap" in emsg.lower():
#             log("Error fetching tweets: 429 Too Many Requests / monthly cap.")
#         else:
#             log(f"Error fetching tweets: {e}")

#     # If we got here, API path yielded nothing or errored.
#     # Decide whether to try snscrape fallback.
#     use_env_scrape = os.getenv("USE_SNSCRAPE") == "1"
#     if use_scrape_flag or use_env_scrape:
#         query = os.getenv("SCRAPE_QUERY", keyword)
#         limit = int(os.getenv("SCRAPE_LIMIT", str(max(count, 100))))
#         log("Falling back to snscrape (no Twitter API)...")
#         ok = run_snscrape(query, limit=limit)
#         if ok:
#             log(f"Fetched via snscrape fallback. See '{OUTFILE_TXT}' and '{OUTFILE_JSONL}'.")
#             return
#         else:
#             log("snscrape fallback failed.")
#     else:
#         log("Skipping snscrape fallback (enable with --scrape or USE_SNSCRAPE=1).")

#     # Final check: if we already have old files from a previous run, keep pipeline alive
#     if os.path.exists(OUTFILE_TXT) or os.path.exists(OUTFILE_JSONL):
#         log("No fresh data, but existing tweet files found—downstream analysis can still run.")
#         return

#     # Nothing to analyze; exit non-zero if you want your CI to flag it
#     sys.exit(1)

# if __name__ == "__main__":
#     main()

# fetch_tweets.py  — portable outputs + robust snscrape fallback

import os
import sys
import re
import json
import shlex
import subprocess
from datetime import datetime
from neo4j import GraphDatabase

import tweepy
from twitter_setup import client  # Tweepy v2 Client
from langdetect import detect, LangDetectException

# -------------------------------------------------------------------
# Paths: write/read next to this script so macOS/Windows/VS Code match
# -------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTFILE_TXT = os.path.join(SCRIPT_DIR, os.environ.get("OUTFILE_TXT", "raw_tweets.txt"))
OUTFILE_JSONL = os.path.join(SCRIPT_DIR, os.environ.get("OUTFILE_JSONL", "tweets.jsonl"))

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

from neo4j import GraphDatabase

# Neo4j database credentials
URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

def store_raw_tweets(records, keyword, username=None):
    """
    Store fetched tweets into Neo4j as :Tweet nodes.
    
    Each tweet will be stored with text, ID, keyword, language, and timestamp.
    Optionally connects the tweet to a :USER node via [:FETCHED].
    """

    if not records:
        print("No tweet records to insert.")
        return

    # Connect to Neo4j
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        def insert_tweet(tx, tweet, keyword, username):
            """
                Create the keyword node if it doesn't exist, (MERGE)
                Create the raw_tweet node with the tweet
                Create the relationship between the keyword and the tweet
                Create the relationship between the user and the keyword
            """
            query = """
                MERGE (t:Tweet {id: $id})
                ON CREATE SET
                    t.text = $text,
                    t.keyword = $keyword,
                    t.language = $language,
                    t.created_at = datetime()
                WITH t
                OPTIONAL MATCH (u:USER {username: $username})
                MERGE (u)-[:FETCHED]->(t)
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

        driver.close()
        print(f"Successfully inserted {len(records)} tweets into Neo4j.")


# ------------------------------
# Fallback via snscrape (no API)
# ------------------------------
def run_snscrape(query: str, limit: int = 100) -> bool:
    """
    Requires: pip install snscrape
    Uses the same Python interpreter to avoid PATH issues on macOS.
    Produces OUTFILE_JSONL + OUTFILE_TXT.
    """
    cmd = [
        sys.executable, "-m", "snscrape",
        "--jsonl", "--max-results", str(int(limit)),
        "twitter-search", query,
    ]
    log("Running snscrape: " + " ".join(shlex.quote(c) for c in cmd))
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=SCRIPT_DIR
        )
    except FileNotFoundError:
        log("snscrape not available. Install with: pip install snscrape")
        return False

    if proc.returncode != 0:
        log("snscrape failed:\n" + (proc.stderr or ""))
        return False

    jsonl_records = []
    txt_lines = []
    for line in proc.stdout.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = (obj.get("rawContent") or "").strip()
        text = remove_emojis(text).replace("\n", " ")
        if not text or not is_english(text):
            continue
        tweet_id = obj.get("id")
        jsonl_records.append({"id": tweet_id, "text": text})
        txt_lines.append(text)

    if not jsonl_records:
        log("snscrape returned no usable tweets.")
        return False

    write_jsonl(jsonl_records)
    write_txt(txt_lines)
    return True

# ------------------------------
# Twitter API (Tweepy v2 client)
# ------------------------------
def fetch_tweets_twitter(keyword: str, want: int = 25):
    """
    Fetch recent tweets via Twitter API v2.
    - Deduplicate, clean, filter English
    Returns (txt_lines, jsonl_records)
    """
    # Twitter v2 recent search: max_results 10..100
    max_results = min(max(want, 10), 100)

    response = client.search_recent_tweets(query=keyword, max_results=max_results)
    if not response or not response.data:
        return [], []

    seen = set()
    txt_lines = []
    jsonl_records = []

    for tweet in response.data:
        text = (getattr(tweet, "text", "") or "").strip()
        text = remove_emojis(text).replace("\n", " ")
        if not text or not is_english(text) or text in seen:
            continue
        seen.add(text)
        txt_lines.append(text)
        jsonl_records.append({"id": getattr(tweet, "id", None), "text": text})
        if len(txt_lines) >= want:
            break

    return txt_lines, jsonl_records

# ------------------------------
# Orchestrator
# ------------------------------
def main():
    # CLI:
    #   python fetch_tweets.py "your keywords" --count 25
    # Fallback:
    #   python fetch_tweets.py "your keywords" --scrape
    # Or env:
    #   USE_SNSCRAPE=1 SCRAPE_LIMIT=200 SCRAPE_QUERY="from:nytimes lang:en"
    if len(sys.argv) < 2:
        log('No keyword provided. Example: python fetch_tweets.py "python lang:en"')
        sys.exit(0)

    keyword = sys.argv[1]
    username = sys.argv[2]
    count = 25
    use_scrape_flag = "--scrape" in sys.argv

    if "--count" in sys.argv:
        try:
            count = int(sys.argv[sys.argv.index("--count") + 1])
        except Exception:
            pass

    log("Fetching tweets for sentiment analysis...")
    log("2 we're here")
    try:
        log("Using Twitter API v2...")
        txt_lines, jsonl_records = fetch_tweets_twitter(keyword, want=count)
        if txt_lines:
            write_txt(txt_lines)
            write_jsonl(jsonl_records)
            _digits = len(str(len(txt_lines)))
            log("\nTweets Fetched:\n")
            for i, line in enumerate(txt_lines, 1):
                log(f"{str(i).rjust(_digits)}. {line}")
            log(f"\nSaved {len(txt_lines)} tweets to '{OUTFILE_TXT}' and '{OUTFILE_JSONL}'.")
            return
        else:
            log("No suitable English tweets found via API.")

    except Exception as e:
        emsg = str(e)
        if "429" in emsg or "Too Many Requests" in emsg or "cap" in emsg.lower():
            log("Error fetching tweets: 429 Too Many Requests / monthly cap.")
        else:
            log(f"Error fetching tweets: {e}")

    # API path yielded nothing or errored -> decide on fallback
    use_env_scrape = os.getenv("USE_SNSCRAPE") == "1"
    if use_scrape_flag or use_env_scrape:
        query = os.getenv("SCRAPE_QUERY", keyword)
        limit = int(os.getenv("SCRAPE_LIMIT", str(max(count, 100))))
        log("Falling back to snscrape (no Twitter API)...")
        ok = run_snscrape(query, limit=limit)
        if ok:
            log(f"Fetched via snscrape fallback. See '{OUTFILE_TXT}' and '{OUTFILE_JSONL}'.")
            return
        else:
            log("snscrape fallback failed.")
    else:
        log("Skipping snscrape fallback (enable with --scrape or USE_SNSCRAPE=1).")

    # Keep pipeline alive if previous data exists
    if os.path.exists(OUTFILE_TXT) or os.path.exists(OUTFILE_JSONL):
        log("No fresh data, but existing tweet files found—downstream analysis can still run.")
        return

    sys.exit(1)

if __name__ == "__main__":
    main()

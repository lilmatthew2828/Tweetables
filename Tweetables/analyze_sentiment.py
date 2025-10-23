import os, re, shutil
from typing import List, Tuple

# Paths & NLTK data location (project-local so Windows/macOS behave the same)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NLTK_DIR   = os.path.join(SCRIPT_DIR, "nltk_data")
RAW_PATH   = os.path.join(SCRIPT_DIR, "raw_tweets.txt")
CLEAN_PATH = os.path.join(SCRIPT_DIR, "cleaned_tweets.txt")
OUT_PATH   = os.path.join(SCRIPT_DIR, "tweet_analysis_results.txt")

os.makedirs(NLTK_DIR, exist_ok=True)
os.environ.setdefault("NLTK_DATA", NLTK_DIR)

import nltk

def _ensure_nltk():
    """Ensure required NLTK resources exist; repair known punkt corruption."""
    # If a corrupted punkt exists (PY3_tab), remove the whole punkt dir.
    bad_punkt_marker = os.path.join(NLTK_DIR, "tokenizers", "punkt", "PY3_tab")
    if os.path.exists(bad_punkt_marker):
        shutil.rmtree(os.path.join(NLTK_DIR, "tokenizers", "punkt"), ignore_errors=True)

    needs = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),   # correct: separate resource, not punkt/PY3_tab
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
        ("corpora/words", "words"),
        ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
        ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
    ]
    missing = []
    for path, pkg in needs:
        try:
            nltk.data.find(path)
        except LookupError:
            missing.append(pkg)
    for pkg in missing:
        nltk.download(pkg, download_dir=NLTK_DIR, quiet=True, raise_on_error=True)

_ensure_nltk()

# Safe wrappers (so missing resources never hard-crash)
from nltk import word_tokenize as _wt, pos_tag as _pt

def safe_word_tokenize(text: str) -> List[str]:
    try:
        return _wt(text)
    except Exception:
        return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)

def safe_pos_tag(tokens: List[str], lang: str = "eng"):
    try:
        return _pt(tokens, lang=lang)
    except Exception:
        return [(t, "NN") for t in tokens]

# ---------- Imports that depend on corpora ----------
import string
from nltk.corpus import stopwords, words as _words, wordnet
from nltk.stem import WordNetLemmatizer

try:
    from spellchecker import SpellChecker
    _SPELLCHECK = True
except Exception:
    _SPELLCHECK = False

# ---------- Initialize tools / corpora (with graceful fallbacks) ----------
try:
    stop_words = set(stopwords.words("english"))
except Exception:
    stop_words = set()

lemmatizer = WordNetLemmatizer()

try:
    english_vocab = set(w.lower() for w in _words.words())
except Exception:
    english_vocab = set()

spell = SpellChecker() if _SPELLCHECK else None

# ---------- Slang / shorthand ---------- # Slang List & Sentiment Dictionary Updated by Day Ekoi

slang_whitelist = {"u", "dm", "rn", "pls", "idk", "lol", "brb", "gtg", "lmao", "omg", "tbh", "afaik", "imho", "af", "iykyk", "lmfao", "nbs", "ngl", "smh"}
shorthand_map = {
    "u": "you",
    "dm": "direct message",
    "rn": "right now",
    "pls": "please",
    "idk": "i don't know",
    "lol": "laugh out loud",
    "gtg": "got to go",
    "brb": "be right back",
    "lmao": "laughing my ass off",
    "omg": "oh my god",
    "tbh": "to be honest",
    "afaik": "as far as i know",
    "imho": "in my humble opinion",
    "af": "as fuck",
    "iykyk": "if you know you know",
    "lmfao": "laughing my ass off",
    "nbs": "No Bullshit",
    "ngl": "Not going to lie",
    "smh": "shaking my head"
}

# ---------- Sentiment dictionary (unchanged from your version) ----------
sentiment_dict = {
    "masterpiece": 5, "blockbuster": 5, "must-watch": 5, "award-worthy": 5, "oscar-worthy": 5,
    "breathtaking": 5, "phenomenal": 5, "spectacular": 5, "stunning": 5, "incredible": 5, "legendary": 5,
    "groundbreaking": 5, "emotionally-powerful": 5, "iconic": 5, "revolutionary": 5, "perfection": 5,
    "unforgettable": 5, "flawless": 5, "timeless": 5, "brilliantly-crafted": 5, "peak-cinema": 5, "love": 5,
    "epic": 4, "amazing": 4, "awesome": 4, "brilliant": 4, "fantastic": 4,
    "excellent": 4, "outstanding": 4, "thrilling": 4, "wonderful": 4, "mind-blowing": 4,
    "gripping": 4, "electrifying": 4, "remarkable": 4, "heartwarming": 4, "thought-provoking": 4,
    "well-acted": 4, "visually-striking": 4, "inspiring": 4, "emotional": 4, "hilarious": 4,
    "motivating": 4, "joyful": 4, "rewarding": 4, "uplifting": 4, "refreshing": 4,
    "enjoyable": 4, "powerful": 4, "mind-expanding": 4, "captivating": 4, "masterfully-directed": 4,
    "visually-stunning": 4, "tight-script": 4, "brilliant-performance": 4, "moving": 4, "elegant": 4,
    "well-paced": 4, "immersive": 4, "emotional-journey": 4, "genius": 4,
    "beautiful": 4, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "great": 3, "impressive": 3, "superb": 3, "entertaining": 3, "exciting": 3,
    "intense": 3, "high-octane": 3, "cinematic": 3, "riveting": 3, "charming": 3,
    "engaging": 3, "cult-classic": 3, "fun": 3, "cool": 3, "strong": 3,
    "well-done": 3, "solid": 3, "visually-pleasing": 3, "watchable": 3, "stylish": 3,
    "well-written": 3, "clever": 3, "artistic": 3, "emotion-filled": 3, "smart": 3,
    "balanced": 3, "great-dialogue": 3, "unique": 3, "worthy": 3, "likeable": 3,
    "fun-ride": 3, "touching": 3, "laugh-out-loud": 3, "witty": 3, "feel-good": 3,

     # 13 additional Positive words 
    "Radiant": 4, "Triumphant": 5, "Delightful": 4, "Impactful": 4, "Enchanting": 4, "Invigorating": 4, 
    "Transformative": 5, "Heartening": 4, "Exhilarating": 5, "Exuberant": 4, "Vibrant": 4, "Jaw-dropping": 5, 

    # Positive AAVE/Ebonics Words
    "ate": 4, "bussin": 4, "chewed": 4, "fly": 3, "fye": 4, "gas": 4, "goat": 5, "its giving": 3,
    "lit": 4, "on point": 4, "serving": 3, "slaps": 4, "snatched": 3, "tea": 3,

    "okay": 0, "neutral": 0, "average": 0, "decent": 1, "plain": 1,
    "standard": 1, "typical": 0, "moderate": 1, "simple": 1, "fine": 1,
    "passable": 1, "straightforward": 1, "uncomplicated": 1, "serviceable": 1, "middle-of-the-road": 0,
    "meh": 0, "acceptable": 1, "normal": 1, "basic": 1, "regular": 1,
    "expected": 1, "predictable": -1, "forgettable": -1, "formulaic": -1, "plain-jane": 0, "scary": -1, "surprised": 1,

   # 8 Expanded Neutral words
   "unremarkable": 0, "mundane": 0, "routine": 0, "typical": 0, "uncomplicated": 1, "conventional": 1, "tolerable": 1, "generic": 0,


  # Neural AAVE/Ebonics Words
  "bet": 0, "chile": 0, "fasho": 0, "girl": 0, "gurl": 0, "gworl": 0, "highkey": 1, "ight": 0, "ite": 0, "lowkey": 0,
  "merch": 0, "no cap": 2, "no shade": 0, "word": 0,

    "mediocre": -1, "slow": -2, "uninspired": -2, "cliché": -2, "unrealistic": -2, "dry": -2, "flat": -2,
    "underdeveloped": -2, "confusing": -2, "lackluster": -2, "awkward": -2, "weak": -2, "repetitive": -2,
    "safe": -2, "thin": -2, "shaky": -2, "clunky": -2, "overused": -2, "dull": -3, "unoriginal": -3,
    "underwhelming": -3, "overrated": -3, "cheesy": -3, "forced": -3, "messy": -3, "lifeless": -3,
    "dragging": -3, "plot holes": -3, "wooden acting": -3, "bad CGI": -3, "annoying": -3,
    "frustrating": -3, "meaningless": -3, "empty": -3, "poorly-executed": -3, "disjointed": -3,
    "nonsensical": -3, "ridiculous": -3, "over-the-top": -3, "flat-characters": -3, "exaggerated": -3,
    "boring": -4, "disappointing": -4, "flop": -4, "cringe": -4, "waste": -4,
    "waste-of-time": -4, "cringeworthy": -4, "shocking": -4, "disturbing": -4,
    "painful": -5, "horrible": -5, "terrible": -5, "trash": -5, "worst": -5,
    "atrocious": -5, "devastating": -5, "horrific": -5, "disgusting": -5, "hate": -5,
    "angry": -5, "unwatchable": -5, "nauseating": -5, "garbage": -5, "insulting": -5,
    "anxious": -2, "terrifying": -3, "tense": -1, "tearjerker": 4, "nostalgic": 1,

    "love": 5, "hate": -5, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4,
    "frustrated": -4, "disgusting": -5, "horrific": -5, "devastating": -5, "shocking": -4,
    "unbelievable": -3, "scary": -3, "disturbing": -4,

    # 13 Expanded Negative Words
    "grim": -3, "weak-plot": -3, "incoherent": -3, "meh": 0, "bleh": -1, "abysmal": -5, "dreadful": -5, "horrendous": -5, "pathetic": -4, "pitiful": -4, "chaotic": -3, "bland": -2, 
    "terrible-acting": -4,

    # Negative AAVE/Ebonics Words
    "big mad": -3, "cap": -3, "cappin": -3, "flop": -4, "mid": -2, "pressed": -2, "salty": -2, "shade": -2, "trippin": -2,

    "fire": 4, "goat": 5, "slaps": 4, "based": 4,
    "wack": -3, "overhyped": -3, "underrated": 3, "slept-on": 3, "dead": -3,
    "chef’s-kiss": 5, "vibes": 3, "badass": 4, "yawn": -3, "lit": 4,
    "banger": 4, "peak": 4, "goofy": -2, "corny": -3, "sus": -2,
    "hard": 4, "rage": 3, "on-point": 4, "buzz": 2, "flop": -4,
    "sci-fi": 2, "rom-com": 2, "horror": 1, "thriller": 2, "documentary": 1,
    "animation": 2, "drama": 1, "action-packed": 4, "mystery": 2, "psychological": 2,
    "dark": -1, "light-hearted": 3, "gory": -2, "family-friendly": 3, "noir": -1,
    "campy": -2, "twist": 2, "genuine": 3, "cheesy-dialogue": -3, "flashy": 2,
    "breaking": 2, "reaction": 2, "scandal": -3, "attack": -3,
    "urgent": -2, "exposed": -3, "crisis": -3, "controversial": -3, "rumor": -2,
    "debate": -1, "insane": 3, "leak": 1, "announcement": 2, "performance": 2,
    "directorial-debut": 2, "ensemble-cast": 2, "character-driven": 3, "story-driven": 3, "over-indulgent": -2,
    "melodramatic": -2, "heavy-handed": -2, "understated": 2, "visionary": 4, "self-aware": 3,
    "raw": 3, "elevated": 3, "cinematography": 3, "editing": 2, "score": 2
}

# ---------- Utilities ----------
def get_wordnet_pos(treebank_tag: str):
    if treebank_tag.startswith("J"): return wordnet.ADJ
    if treebank_tag.startswith("V"): return wordnet.VERB
    if treebank_tag.startswith("N"): return wordnet.NOUN
    if treebank_tag.startswith("R"): return wordnet.ADV
    return wordnet.NOUN

def clean_tweet(tweet: str) -> List[str]:
    t = tweet.lower()

    # 1) Expand shorthand first
    for w, repl in shorthand_map.items():
        t = re.sub(rf"\b{re.escape(w)}\b", repl, t)

    # 2) Strip links, rt, mentions, hashtags, digits, punctuation
    t = re.sub(r"rt\s+", "", t)
    t = re.sub(r"http\S+|www\S+|https\S+", "", t)
    t = re.sub(r"#\w+", "", t)
    t = re.sub(r"@\w+", "", t)
    t = re.sub(r"\d+", "", t)
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t).strip()

    # 3) Tokenize (safe)
    tokens = safe_word_tokenize(t)

    # 4) Custom blacklist
    blacklist = {"aku", "gama"}
    tokens = [w for w in tokens if w not in blacklist]

    # 5) POS tagging + lemmatize
    tags = safe_pos_tag(tokens)
    cleaned = []
    for w, tag in tags:
        if w in slang_whitelist:
            cleaned.append(w)
            continue

        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(w, wn_pos)

        candidate = lemma

        # 🔑 If lemmatization would break a known sentiment word,
        # keep the original token instead of the lemma.
        if (lemma not in sentiment_dict) and (w in sentiment_dict):
            candidate = w

        # stopwords/vocab/spell checks (all optional-safe)
        if candidate in stop_words:
            continue
        if len(candidate) <= 1 and candidate not in shorthand_map:
            continue

        ok_vocab = True
        if english_vocab:
            ok_vocab = (candidate in english_vocab)
        if not ok_vocab and spell:
            ok_vocab = (spell.correction(candidate) == candidate)

        if ok_vocab:
            cleaned.append(candidate)

    return cleaned

def format_cleaned_text(tokens: List[str]) -> str:
    return " ".join(tokens)

def analyze_sentiment(tokens: List[str]) -> Tuple[str, int]:
    score = sum(sentiment_dict.get(tok, 0) for tok in tokens)
    if score > 0:  return "Positive", score
    if score < 0:  return "Negative", score
    return "Neutral", score

# ---------- Load, process, save ----------
# (Replaced: file I/O → Neo4j integration)
from neo4j import GraphDatabase

URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

driver = GraphDatabase.driver(URI, auth=AUTH)

def _fetch_raw_tweets_without_cleaned(skip: int, limit: int):
    cypher = """
    MATCH (r:Tweet)
    WHERE NOT (r)-[:HAS_CLEANED]->(:CleanedTweet)
      AND r.text IS NOT NULL
      AND trim(r.text) <> ''
    RETURN elementId(r) AS rid, r.text AS text
    SKIP $skip LIMIT $limit
    """
    records, _, _ = driver.execute_query(cypher, {"skip": skip, "limit": limit})
    return [{"rid": r["rid"], "text": r["text"]} for r in records]

def write_cleaned_tweets(rows):
    cypher = """
    UNWIND $rows AS row
    MATCH (r:Tweet) WHERE elementId(r) = row.rid
    MERGE (c:CleanedTweet { cleaned_tweet: row.clean })
    SET c.tokens     = row.tokens,
        c.sentiment  = row.label,
        c.score      = row.score
    MERGE (r)-[:HAS_CLEANED]->(c)
    """
    driver.execute_query(cypher, {"rows": rows})

# (Optional) quick visibility into remaining work
count_q = """
MATCH (r:Tweet)
WHERE NOT (r)-[:HAS_CLEANED]->(:CleanedTweet)
  AND r.text IS NOT NULL
  AND trim(r.text) <> ''
RETURN count(*) AS n
"""
records, _, _ = driver.execute_query(count_q)
print("Unprocessed candidates:", records[0]["n"])

output_lines = []
cleaned_tweet_lines = []

total_processed = 0
page = 0

while True:
    batch = _fetch_raw_tweets_without_cleaned(skip=page * 500, limit=500)
    if not batch:
        break

    prepared = []
    for row in batch:
        raw = row["text"]
        cleaned_tokens = clean_tweet(raw)
        cleaned_text = format_cleaned_text(cleaned_tokens)
        label, score = analyze_sentiment(cleaned_tokens)

        line = (
            f"RAW: {raw}\n"
            f"CLEANED: {cleaned_text}\n"
            f"SENTIMENT: {label} (Score: {score})\n"
            + "-" * 50
        )
        print(line)
        output_lines.append(line)
        cleaned_tweet_lines.append(cleaned_text)

        prepared.append({
            "rid": row["rid"],          # elementId(r) STRING
            "clean": cleaned_text,
            "tokens": cleaned_tokens,
            "label": label,
            "score": score,
        })

    for i in range(0, len(prepared), 200):
        write_cleaned_tweets(prepared[i:i+200])

    total_processed += len(prepared)
    page += 1
    print(f"Processed page {page}: {len(prepared)} tweets (total {total_processed})")

driver.close()
print(f"Analysis complete! Wrote {total_processed} cleaned tweets to Neo4j. Full results saved to '{OUT_PATH}'.")
# --- end block ---


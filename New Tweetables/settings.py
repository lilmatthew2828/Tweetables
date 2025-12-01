# settings.py
# Configuration settings for the application
# (shared constants & helpers) 
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = BASE_DIR
NLTK_DIR   = os.path.join(SCRIPT_DIR, "nltk_data")
os.makedirs(NLTK_DIR, exist_ok=True)

# Image used on Login/Signup
LOGO_PATH = os.path.join(BASE_DIR, "unnamed.png")

# Neo4j config (you can swap to env-based later)
URI  = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

def subprocess_env():
    env = dict(os.environ)
    env["NLTK_DATA"] = NLTK_DIR
    return env
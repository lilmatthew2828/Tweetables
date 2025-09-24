import tweepy
import os
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

#retrieve API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Needed for API v2

# Ensure variables are loaded
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    raise ValueError("Missing API credentials. Check your .env file.")

#print(f"API_KEY: {API_KEY}")
#print(f"API_SECRET: {API_SECRET}")
#print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
#print(f"ACCESS_SECRET: {ACCESS_SECRET}")
#print(f"BEARER_TOKEN: {BEARER_TOKEN}")

#authenticate to twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create API object
api = tweepy.API(auth, wait_on_rate_limit = True)

#authenticate using API v2 (for fetching tweets)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# test authentication
try:
    user = api.verify_credentials()
    print(f"Authentication successful! Logged in as: {user.name}")
except Exception as e:
    print(f"Authentication failed: {e}")
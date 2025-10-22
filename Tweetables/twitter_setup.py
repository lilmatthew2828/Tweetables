import tweepy
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from neo4j import GraphDatabase #imports database from neo4j

URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

#load environment variables from .env file
load_dotenv()

def get_twitter_client(username):
    master_key = os.getenv("MASTER_KEY")
    results = None

    def retrieve_credtials(driver, username):
        query = """ 
            Match (u:USER {username: $username})
            RETURN u.enc_api_key AS enc_api_key,
                   u.enc_api_secret AS enc_api_secret,
                   u.enc_access_token AS enc_access_token,
                   u.enc_access_secret AS enc_access_secret,
                   u.enc_bearer_token AS enc_bearer_token
        """
        records, _, _ = driver.execute_query(query, username = username)
        return records

    with GraphDatabase.driver(URI, auth= AUTH) as driver:
        driver.verify_connectivity()
        results = retrieve_credtials(driver, username)
        driver.close()

    enc_api_key = results[0][0]
    enc_api_secret = results[0][1]
    enc_acces_token = results[0][2]
    enc_access_secret = results[0][3]
    enc_bearer_token = results[0][4]

    f = Fernet(master_key)

    api_key = f.decrypt(enc_api_key).decode()
    api_secret = f.decrypt(enc_api_secret).decode()
    acces_token = f.decrypt(enc_acces_token).decode()
    access_secret = f.decrypt(enc_access_secret).decode()
    bearer_token = f.decrypt(enc_bearer_token).decode()

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(acces_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=0)

    client = tweepy.Client(bearer_token=bearer_token)

    return client



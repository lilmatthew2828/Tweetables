import requests
from twitter_setup import BEARER_TOKEN #import bearer token

def check_rate_limit():
    #check twitter APIv2 rate limits manually
    url = "https://api.twitter.com/2/tweets/search/recent?query=AI&max_results=10"
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request succesfull! Checking rate limits...\n")
        print("Headers:", response.headers) #print full headers(includes rate limits)
        print(f"Requests Remaining: {response.headers.get('x-rate-limit-remaining', 'Unknown')}")
        print(f"Rate Limit Resets At: Remaining: {response.headers.get('x-rate-limit-reset', 'Unknown')}")
    else:
        print(f"Error checking rate limit: {response.status_code} - {response.text}")
   
check_rate_limit()
from twitter import client
from pprint import pprint
import pandas as pd
from pathlib import Path
from time import sleep

BEARER="yourtokenhere"
VERBOSE=True
FILENAME="tweets.csv"
subqueries=[
  "politica brasil",
  "politica brasileira",
  "(#politica #brasil)",
  "STF",
  "(Bolsonaro Lula)",
  "(supremo Brasil)"
]
cycle_limit=500000

def fetch_results(next_token=None):
  query = f"{' OR '.join(subqueries)} lang:pt -is:retweet"
  return client.getTweets(
    token=BEARER, 
    q=query,
    count=100,
    next_token=next_token
  ).json()

if __name__ == "__main__":
  first_run=True
  next_token=None
  results=[]
  cycle=0
  total=0
  while(first_run or next_token):
    first_run=False

    print(f"Fetching page {cycle} of tweets. Total: {total}")
    try:
      response=fetch_results(next_token)
    except:
      sleep(60)
      continue
    cycle += 1
    total += 100
    
    if VERBOSE:
      pprint(response)

    data=response['data']
    meta=response['meta']
    results.extend(data)

    next_token=meta['next_token']

    if (len(results) > 1000):
      df = pd.DataFrame.from_dict(results)
      df.to_csv(
        FILENAME,
        mode="a", 
        header=False if Path(FILENAME).exists() else True,
        sep=";",
        encoding="utf-16"
      )
      results=[]
  df = pd.DataFrame.from_dict(results)
  df.to_csv(
    FILENAME,
    mode="a", 
    header=False if Path(FILENAME).exists() else True,
    sep=";",
    encoding="utf-16"
  )
  print("end")
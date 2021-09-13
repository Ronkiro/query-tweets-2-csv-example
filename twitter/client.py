import requests
from urllib.parse import quote

def getTweets(token, q="", count=100, next_token=None):
  headers = {
    "Authorization": "Bearer " + token,
  }

  print("Searching for", q)
  q=quote(q).replace('%20', "+")

  BASE_URL="https://api.twitter.com/2/tweets/search/recent"

  params_list = [
    f"?query={q}",
    f"&max_results={count}"
  ]

  if next_token:
    params_list.append(f"&next_token={next_token}")

  return requests.get(
    url=BASE_URL + ''.join(params_list), 
    headers=headers
  )
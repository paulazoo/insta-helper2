import requests
import json

def get_user_info(username):
  url = "https://www.instagram.com/"+username+"/?__a=1"

  payload = {}
  headers = {
    'Cookie': 'csrftoken=QL5ajpJpIwcKHFpZGpi3oBVbdhhhXOH5; ig_nrcb=1; ig_did=3873CA7F-9A2A-4943-B151-C03FE1E75F01; mid=X4u6gQAEAAGymmGKlUKKLGWPlppt; urlgen="{\\"65.112.8.31\\": 1742}:1kTze5:VLv3ndk9GXtXCzzECQHe9KhFbqE"'
  }

  response = requests.request("GET", url, headers=headers, data = payload)

  res = json.loads(response.text)
  return res['graphql']['user']

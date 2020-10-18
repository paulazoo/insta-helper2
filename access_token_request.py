import requests
from dotenv import load_dotenv
import os

def get_access_token(code):
  load_dotenv()

  CLIENT_ID = os.getenv('CLIENT_ID')
  CLIENT_SECRET = os.getenv('CLIENT_SECRET')

  url = "https://api.instagram.com/oauth/access_token/"

  payload = 'client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET+'&grant_type=authorization_code&redirect_uri=https%3A//congregate.live/auth/&code='+code
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'csrftoken=QL5ajpJpIwcKHFpZGpi3oBVbdhhhXOH5; ig_nrcb=1'
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  print('done')
  print(response.text)

  return response

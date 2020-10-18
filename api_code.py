
from dotenv import load_dotenv
import os

def get_api_code(self):
  load_dotenv()

  CLIENT_ID = os.getenv('CLIENT_ID')

  self.driver.get("https://api.instagram.com/oauth/authorize?client_id="+CLIENT_ID+"&redirect_uri=https://congregate.live/auth/&scope=user_profile,user_media&response_type=code")

  code_url = self.driver.current_url

  code = code_url.split("/?code=",1)[1][:-2]

  return code

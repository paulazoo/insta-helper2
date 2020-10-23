import os
from dotenv import load_dotenv

#selenium
from selenium import webdriver
#keyboard manipulation
from selenium.webdriver.common.keys import Keys
#webdriver options
from selenium.webdriver.chrome.options import Options

#keep track of time
import time
#sound notifications (beeps)
import winsound

#to read and edit excel files
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from access_token_request import get_access_token
from api_code import get_api_code
from ig_requests import get_user_info, get_detailed_user_info

from self_following_extra import self_following_extra_users
from self_following import self_following_users

#class to hold bot functions
class InstaHelp:

  def __init__(self, username, password):
    #set class attributes
    self.username = username
    self.password = password

    #set up chrome driver
    option = Options()

    #stop notif popup
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2 
    })

    #open webdriver chrome browser
    self.driver = webdriver.Chrome(chrome_options=option, executable_path='./chromedriver.exe')

  def use_api(self):
    # code = "AQCoRJ-83jxt7SZLd6tj-NbsUcj1LDGoqTAtA7rWNG8pFpGPotpYGqakHkTOow4_4NXRDpMCQsrTIo-sLIR14LdahhBgVx7q1gyP_5OPi19fmIa3aKgOhLtWj62q2np8A02L3CtKlsg8ZRYl87Q_JLEVhviM7X-4g8-W9fIVvTAgLusFyaQTZxHOM_OU6yeh52kXvRj1XNCbEJbWggFIG_XWGSPf2wifg8Sdb_Hw-rk2fg"
    # code = get_api_code(igpy)

    # access_token_res = get_access_token(code)
    # access_token = access_token_res.access_token
    # api_user_id = access_token_res.user_id
    access_token = "IGQVJWWFEtcWUzbTh6NGpyaXBUSjhFcE9KLW1NS19GbDRZAVHZAkWjBJVHhqUm5XTnR4eVNyNXFRUkRFdzMtUjhLRnRxTVFvcTVxS01jVnQybXpOYmpuYTJaOVlUakxveDQ4ZATQyYkNYYkNVZAEdXRGQyeExWaGUtY1hBRWs0"
    api_user_id = 17841435674911975 # welp. maybe someone else can use

    return access_token, api_user_id

  #define logging in
  def login(self):
    #get instagram login page
    self.driver.get('https://www.instagram.com/accounts/login/')
    #wait to load
    time.sleep(2)
    #find username box and password box by name attribute (from inspect element)
    #then send keys from self.username, self.password
    self.driver.find_element_by_name('username').send_keys(self.username)
    self.driver.find_element_by_name('password').send_keys(self.password)
    #find and click login button as first element with text "Log In" in div (insepct element)
    self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
    #time to load
    time.sleep(3)
    print('logged in')
    try:
      self.driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()
      time.sleep(2)
    except:
      print('No notif button')

  def close_driver(self):
    self.driver.close()
    print('closed out')

  def get_user(self, username):
    user_info = get_user_info(username)
    user_bio = user_info["biography"]

    is_harvard = False
    
    if "harvard" in user_bio or "Harvard" in user_bio:
      is_harvard = True

    return user_info, is_harvard

  def get_user_followers(self, username, follower_count):
    time.sleep(2)
    self.driver.get('https://www.instagram.com/'+username+'/')
    time.sleep(2)
    self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")[0].click()
    time.sleep(2)

    followers = []

    while len(followers) < follower_count:
      follower_els = self.driver.find_elements_by_class_name('FPmhX')
      #get usernames
      more_followers = [i.get_attribute('title') for i in follower_els]
      followers = list(set(followers + more_followers))

      #print number of followers
      print(len(followers))

      # self.driver.execute_script("window.scrollTo(0, window.scrollY + 200);")
      time.sleep(0.5)
    
    #print final number of followers
    print("final followers: "+str(len(followers)))
    return followers
    
  def get_user_following(self, username, following_count):
    time.sleep(2)
    self.driver.get('https://www.instagram.com/'+username+'/')
    time.sleep(2)
    self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")[1].click()
    time.sleep(2)

    following = []

    while len(following) < following_count:
      following_els = self.driver.find_elements_by_class_name('FPmhX')
      #get usernames
      more_following = [i.get_attribute('title') for i in following_els]
      following = list(set(following + more_following))

      #print number of following
      print(len(following))

      element_inside_popup = self.driver.find_element_by_xpath("//div[@class='isgrP']")
      self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element_inside_popup)
      time.sleep(2)
    
    #print final number of followers
    print("final following: " + str(len(following)))
    return following
    
  def get_harvard_friends(self):
    self.driver.get('https://www.instagram.com/crimsoncrew2024/')
    
    self.driver.find_element_by_xpath("//a[@class='-nal3 ']").click()
    time.sleep(2)

    keep_going = True
    while keep_going:
      follow_buttons = self.driver.find_elements_by_xpath("//button[contains(text(), 'Log In')]")

      for btn in follow_buttons:
        try:
          btn.click()
          friend_requests_sent = friend_requests_sent + 1
        except:
          print("An exception occurred")
            
      self.driver.execute_script("window.scrollTo(0, window.scrollY + 200);")
      time.sleep(0.5)

  def visit_peeps(self, peeps, skip_harvard):
    for peep in peeps:
      is_harvard = False

      if skip_harvard:
        user_info, is_harvard = self.get_user(peep)

      if is_harvard == False:
        time.sleep(5)
        self.driver.get('https://www.instagram.com/'+peep+'/')

  def get_cookies(self):
    cookie_dict = {}
    cookie_dict['ig_did'] = self.driver.get_cookie("ig_did")["value"]
    cookie_dict['ig_nrcb'] = self.driver.get_cookie("ig_nrcb")["value"]
    cookie_dict['mid'] = self.driver.get_cookie("mid")["value"]
    cookie_dict['csrftoken'] = self.driver.get_cookie("csrftoken")["value"]
    cookie_dict['ds_user_id'] = self.driver.get_cookie("ds_user_id")["value"]
    cookie_dict['sessionid'] = self.driver.get_cookie("sessionid")["value"]
    cookie_dict['shbid'] = self.driver.get_cookie("shbid")["value"]
    cookie_dict['shbts'] = self.driver.get_cookie("shbts")["value"]
    cookie_dict['rur'] = self.driver.get_cookie("rur")["value"]
    cookie_dict['urlgen'] = self.driver.get_cookie("urlgen")["value"]

    return cookie_dict
  
  def get_detailed_user(self, username, cookies):
    detailed_user_info = get_detailed_user_info(username, cookies)

    return detailed_user_info

  def get_most_recent_pic(self, detailed_user_info):
    pic = detailed_user_info["edge_owner_to_timeline_media"]["edges"][0]["node"]
    pic_timestamp = pic["taken_at_timestamp"]
    pic_url = pic["shortcode"]

    return pic_url, pic_timestamp

  def like_pic(self, pic_url):
    self.driver.get('https://www.instagram.com/p/'+pic_url+'/')
    time.sleep(2)
    
    like_span_el = self.driver.find_element_by_xpath("//span[@class='fr66n']")

    like_svg_aria_label =  like_span_el.find_element_by_xpath(".//*[name()='svg']").get_attribute("aria-label")
    
    if like_svg_aria_label == "Like":
      like_span_el.find_element_by_xpath(".//button[@class='wpO6b ']").click()
      time.sleep(2)


if __name__ == '__main__':
  load_dotenv()
  IG_PASSWORD = os.getenv('IG_PASSWORD')
  IG_USERNAME = os.getenv('IG_USERNAME')

  igpy = InstaHelp(IG_USERNAME, IG_PASSWORD)

  # login
  igpy.login()

  '''
  checkout extra following
  '''
  cookies = igpy.get_cookies()

  with open('cookie_storage.txt', 'w') as f:
    str_cookie = str(cookies)
    f.write(str_cookie)

  extra_following = []
  ignore_extra_following = []
  for peep in self_following_users:
    try:
      detailed_user_info = igpy.get_detailed_user(peep, cookies)
      if peep not in ignore_extra_following and detailed_user_info["follows_viewer"] == False:
        extra_following.append(peep)
    except:
      print(peep)

  with open('self_following_extra.txt', 'w') as f:
    for i in extra_following:
        f.write("%s\n" % i)

  '''
  like followers' most recent pics
  '''
  # cookies = igpy.get_cookies()

  # for peep in self_followers:
    # detailed_user_info = igpy.get_detailed_user(peep, cookies)
    # pic_url, pic_timestamp = igpy.get_most_recent_pic(detailed_user_info)
  
    # 24 hours
    # timestamp = time.time() - 86400
    
    # if pic_timestamp > timestamp: 
    #   # igpy.like_pic(pic_url)


import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which
from bs4 import BeautifulSoup
import time
from ..control_function import slow_typing


class LinkedinscrapSpider(scrapy.Spider):
    name = 'LinkedinScrap'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['https://www.linkedin.com/']

    def __init__(self):
        # chrome set up and run
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.linkedin.com/")

        # username and password read from file
        try:
            file = open('E:\Project Work\Online Content\Scrapy\Project4\LinkedinProfileScrap\LinkedinProfileScrap\confidential_info.txt')
            lines = file.readlines()
            user_email = lines[0]
            user_password = lines[1]
        except:
            pass

        # Search as per slow typing with different element
        username = driver.find_element_by_id("session_key")
        set_username = slow_typing(username, user_email)
        password = driver.find_element_by_id("session_password")
        set_password = slow_typing(password, user_password)
        submit_btn = driver.find_element_by_class_name("sign-in-form__submit-button")
        submit_btn.click()
        time.sleep(20)

        # click profile url
        profile_url = driver.find_element_by_xpath("//div/a[@class='ember-view block']").click()
        time.sleep(60)
        # Click show more button in people also viewed section
        people_also_viewed_show_more = driver.find_element_by_class_name("artdeco-card__actions").click()
        time.sleep(60)

        visited_profile = []
        profile_in_queue = []

        def GetNewProfileIds(soup, profile_in_queue):
            newProfileId = []
            people_also_viewed_html = soup.find('section', {'class':'artdeco-card ember-view mt5'})
            #print(people_also_viewed_html) # return full section html
            people_also_viewed_profile_url = people_also_viewed_html.find_all('a', {'class': 'ember-view display-flex link-without-hover-visited'})
            #print(people_also_viewed_profile_url) # return full anchor as List bcz find_all return List
            for link in people_also_viewed_profile_url:
                #print(link.get('href'))
                profile_link = link.get('href')
                if ((profile_link not in profile_in_queue) and (profile_link not in visited_profile)):
                    newProfileId.append(profile_link)
            return newProfileId # return list


        profile_in_queue = GetNewProfileIds(BeautifulSoup(driver.page_source, "lxml"), profile_in_queue)
        #print(profile_in_queue) # List 

        while profile_in_queue:
            visiting_profile = profile_in_queue.pop() # pop means that it will take the value and remove the value from list and pop index means pop() blank that take the value from last 
            visited_profile.append(visiting_profile)
            visiting_profile_full_link = f"https://www.linkedin.com/{visiting_profile}"
            print(visiting_profile_full_link)
            driver.get(visiting_profile_full_link)
            time.sleep(20)
            try:
                connect_btn = driver.find_element_by_xpath("//div[@class='pvs-profile-actions ']/button").click()
                add_note_btn = driver.find_element_by_xpath("//button[@aria-label='Add a note']").click()
                time.sleep(5)
                message_box = driver.find_element_by_xpath("//textarea[@id='custom-message']")
                custome_message = 'Hi, This is Sami.'
                message_typing = slow_typing(message_box, custome_message)
                time.sleep(5)
                cancle_btn = driver.find_element_by_xpath("//button[@aria-label='Cancel adding a note']").click()
                #send_btn = driver.find_element_by_xpath("//button[@aria-label='Send now']").click()
            except:
                pass
            
    def parse(self, response):
        pass

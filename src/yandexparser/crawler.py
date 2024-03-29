from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
import os
import json

URL = 'https://yandex.ru/maps'

LINK_XPATH = "//div[contains(@class,'_type_business')]//a[contains(@class,'search-snippet-view')]"


class LinksCrawler:

    def __init__(self, city, business_cat, area = '', driver=None) -> None:
        self.city = city
        self.business_cat = business_cat
        self.area = area
        self.driver = webdriver.Chrome()

    def scroll_to_bottom(self):
        scroll_by = 100
        self.driver.execute_script(f"document.getElementsByClassName('scroll__container')[0].scrollBy(0,{scroll_by})")

    def scrollbar_bottom_check(self):
        scroll_height = self.driver.execute_script("return document.getElementsByClassName('scroll__container')[0].clientHeight")
        scroll_top = self.driver.execute_script("return document.getElementsByClassName('scroll__container')[0].scrollTop")
        content_height = self.driver.execute_script("return document.getElementsByClassName('scroll__content')[0].clientHeight")
        total_height = scroll_top + scroll_height

        if total_height == content_height:
            return True
        
    def links_scraper(self, business_links):
        elements=self.driver.find_elements(By.XPATH, LINK_XPATH)
        links = [el.get_attribute('href') for el in elements]
        return list(set(links + business_links))

    def search(self):
        search_form = self.driver.find_element(By.XPATH, "//input[@class='input__control _bold']")
        search_form.send_keys(f'{self.city},{self.area},{self.business_cat}')
        search_form.send_keys(Keys.ENTER)

    def links_writer(self, links):
        dir = '../links'
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(f'{dir}/{self.city} - {self.area + " -" if self.area else ""} {self.business_cat}.json', 'w') as f:
            json.dump({'links': links}, f)

    def run(self):
        try:
            self.driver.get(URL)
            self.driver.maximize_window()
            self.search()
            sleep(5)

            business_links = []

            while True:
                self.scroll_to_bottom()
                sleep(0.5)
                business_links = self.links_scraper(business_links)
            
                if self.scrollbar_bottom_check():
                    break


            self.links_writer(business_links)

        except Exception as ex:
            print(ex)
            self.driver.quit()

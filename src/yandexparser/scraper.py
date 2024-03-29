import requests
from bs4 import BeautifulSoup

HEADERS = {
    'accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
    'referer': 'https://www.google.com/',
    'Host': 'api.passport.yandex.ru',
    'Origin': 'https://yandex.ru',
    'Referer': 'https://yandex.ru/maps',
    'Sec-Cookie-Deprecation': 'label_only_2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
}


class InfoScraper:

    def __init__(self, link, soup=None, driver=None) -> None:
        self.link = link
        self.soup = soup

    def make_soup(self):

        response = requests.get(self.link, headers=HEADERS)
        print(response.status_code)
        content = response.text

        self.soup = BeautifulSoup(content, 'lxml')

    def get_name(self):
        try:
            title = self.soup.find('h1').get_text()
            return title
        except:
            return ''

    def get_address(self):
        try:
            address = self.soup.find('a', class_='orgpage-header-view__address').get_text()   
            return address
        except:
            return ''
    
    def get_phone(self):
        try:
            phone = self.soup.find('div', class_='orgpage-phones-view__phone-number').get_text()
            return phone
        except:
            return ''
        
    def get_website(self):
        try:
            website = self.soup.find('span', class_='business-urls-view__text').get_text()
            return website
        except:
            return ''
        
    def get_social_links(self):
        try:
            social_links = {link.a['aria-label'].split(',')[-1].strip():link.a['href'] for link in self.soup.find_all('div', class_='business-contacts-view__social-button')}
            return social_links
        except:
            return []
        
    def get_category(self):
        try:
            category = self.soup.find_all('a', class_='breadcrumbs-view__breadcrumb _outline')[-1].get_text()
            return category
        except:
            return ''
        
    def get_rating(self):
        try:
            rating = self.soup.find('span', class_='business-rating-badge-view__rating-text').get_text()
            return rating
        except:
            return ''
        
    def get_opening_hours(self):
        try:
            opening_hours = [i['content'] for i in self.soup.find_all('meta', itemprop='openingHours')]
            return opening_hours
        except:
            return []
        
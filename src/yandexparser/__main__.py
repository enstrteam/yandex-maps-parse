from yandexparser.crawler import LinksCrawler
from yandexparser.scraper import InfoScraper
from yandexparser.parser import InfoParser

import json

def main():

    city = 'москва'
    area = 'экспострой'
    search_category = 'паркет'

    crawler = LinksCrawler(city, search_category, area)
    crawler.run()

    file = f'{city} - {area + " -" if area else ""} {search_category}.json'

    with open(f'../links/{file}', 'r') as f:
        urls = json.loads(f.read())

    for url in urls['links']:
        scraper = InfoScraper(url)
        scraper.make_soup()
        
        name = scraper.get_name()
        phone = scraper.get_phone()
        address = scraper.get_address()
        website = scraper.get_website()
        social_links = scraper.get_social_links()
        category = scraper.get_category()
        rating = scraper.get_rating()
        opening_hours = scraper.get_opening_hours()

        data = {
            'category': category,
            'name': name,
            'phone': phone,
            'address': address,
            'rating': rating,
            'website': website,
            'social_links': social_links,
            'opening_hours': opening_hours
        }

        parser = InfoParser(data)
        parser.output(city=city, category=search_category, area=area)

        print(name, category, phone, address, website, social_links, rating, opening_hours)
    
    

if __name__ == '__main__':
    main()
import os
import logging
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider(scrapy.Spider):
    # Name of your spider
    name = "Bookingspider"

    # Starting URL
    start_urls = ['https://www.booking.com/index.fr.html']
    
    cities = df['name']
    # Parse function for form request
    def parse(self, response):
        # FormRequest used to make a search in each of the 35 cities
        for city in cities :
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'input#:re:.eb46370fe1': city},
                callback=self.after_search
        )

    # Callback used after login
    def after_search(self, response):
        results= response.xpath('//*[@id="bodyconstraint-inner"]/div[4]/div/div[2]/div[3]/div[2]/div[2]/div[3]')
        
        for r in results :
            yield {
                
        'name' : r.xpath('div[3]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
        'url' : r.xpath('div[3]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a').attrib['href'],
        'score' : r.xpath('div[3]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]/text()').get(),
        
                
    
            }
            
        # Select the NEXT button and store it in next_page
        try:
            next_page = response.xpath('//*[@id="bodyconstraint-inner"]/div[4]/div/div[2]/div[3]/div[2]/div[2]/div[4]/div[2]/nav/nav/div/div[3]/button/a').attrib["href"] 
        except KeyError:
            logging.info('No next page. Terminating crawling process.')
        else:
            yield response.follow(next_page, callback=self.after_search)

# Name of the file where the results will be saved
filename = "hotels.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir():
        os.remove(filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()
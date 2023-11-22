import scrapy
#import random
from rymhurtownie.items import RymChart
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['rateyourmusic.com']
    #pages = range(1, 1)  #one page is 40 albums per year
    years = range(2002, 2022)  # a nice 20 year span
      # ["https://rateyourmusic.com/charts/top/album/" + str(year) + "/" + str(page)
    #put your proxy in here - rateyourmusic.com usually bans ip's that are scraping its pages - i used proxy.scrapeops.io for testing this and it worked
    start_urls = [proxy + str(year) + "%2F"
        for year in years]
    #to not get banned again // didnt work anyway rofl
    # random.seed()
    # random.shuffle(start_urls)


    def parse(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        for albums in response.css("div.object_release"):
            item = RymChart()
            item['artists'] = albums.css("a.artist span.ui_name_locale_original::text").get()
            item['title'] = albums.css("a.release span.ui_name_locale_original::text").get()
            item['year'] = albums.css("div.page_charts_section_charts_item_date span::text").get()
            item['genres'] = albums.css("div.page_charts_section_charts_item_genres_primary a.genre::text").getall()
            item['average_rating'] = albums.css("span.page_charts_section_charts_item_details_average_num::text").get()

            yield item
       
def errback_httpbin(self, failure):
    # log all failures
    self.logger.error(repr(failure))

    # in case you want to do something special for some errors,
    # you may need the failure's type:

    if failure.check(HttpError):
        # these exceptions come from HttpError spider middleware
        # you can get the non-200 response
        response = failure.value.response
        self.logger.error('HttpError on %s', response.url)

    elif failure.check(DNSLookupError):
        # this is the original request
        request = failure.request
        self.logger.error('DNSLookupError on %s', request.url)

    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        self.logger.error('TimeoutError on %s', request.url)

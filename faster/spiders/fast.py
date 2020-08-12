import scrapy
from scrapy import signals
from time import time
from pprint import pprint
import os
import re
from datetime import datetime

try:
  from fast.spiders.ORM import Nadlansale

except Exception as e:
  try:
    from ORM import Nadlansale, Operations

  except Exception as e:
    pass


class RootSpider(scrapy.Spider):
  name = "root"
  results = []


  def start_requests(self):
    start_url = 'https://www.ad.co.il/nadlansale?pageindex={}'
    self.ids = Operations.GetIDDict()

    for idx in range(1,10000):
      yield scrapy.Request(url=start_url.format(idx), callback=self.parser, errback=self.errbacktest, meta={'root': idx})

  def parser(self, response):
    #response.meta.get('root')
    ads = response.xpath("//div[@data-id]")

    for ad_div in ads:
      result = {}
      result['id'] = int(ad_div.xpath("@data-id").extract_first())

      if result['id'] in self.ids:
        continue

      result["url"] = 'https://www.ad.co.il/ad/{}'.format(ad_div.xpath("@data-oid").extract_first())
      result['price'] = ad_div.xpath("@data-price").extract_first()
      result['contact'] = ad_div.xpath("@data-contact").extract_first()
      result['area'] = ad_div.xpath('@data-salearea').extract_first()
      result['city'] = ad_div.xpath("@data-city").extract_first()
      result['created'] = datetime.fromtimestamp(int(str(ad_div.xpath('@data-created').extract_first())[0:-3]))

      phone = ad_div.xpath("@data-phone").extract_first().split('/')
      result['phone1'] = phone[0].replace('-', '')
      result['phone2'] = phone[1].replace('-', '') if len(phone) == 2 else ''

      result['description'] = ad_div.xpath("@data-desc").extract_first().replace("\n", '')

      result['available'] = ad_div.xpath('@data-enterdate').extract_first()
      result['latitude'] = ad_div.xpath('@data-lat').extract_first()
      result['longitude'] = ad_div.xpath('@data-lon').extract_first()
      result['type'] = ad_div.xpath('@data-saletype').extract_first()
      result['size'] = ad_div.xpath('@data-areasize').extract_first()
      result['neighbourhood'] = ad_div.xpath('@data-hood').extract_first()

      self.ids[result['id']] = None
      self.results.append(Nadlansale(result))

    pass

  def errbacktest(self, failiure):
    pass

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super().from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    return spider

  def spider_closed(self, spider):
    Operations.BulkUpdate(self.results)

if __name__ == "__main__":
  pass
from scrapy.spiders import SitemapSpider
from gwport.items import Items
from scrapy.selector import Selector
import csv


class MySpider(SitemapSpider):
    name = "scraper"
    sitemap_urls = ["https://www.ato.gov.au/sitemap.xml"]

    sitemap_follow = ["/Super/"]

    sitemap_rules = [(r"ato.gov.au/Super/", "parse")]

    def parse(self, response):
        item = Items()
        sel = Selector(response)

        item["url"] = response.url
        item['title'] = sel.xpath('/html/head/title/text()').extract()[
            0].replace("\r", "").replace("\t", "").replace("\n", "")
        item["text"] = "".join(response.css("p::text").getall())

        # save URL for CSV
        with open("./output.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([response.url])

        yield item

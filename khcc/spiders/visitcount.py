# -*- coding: utf-8 -*-
import sys
import scrapy
import urlparse
import re
import os
import datetime
from scrapy.utils.project import get_project_settings
import pytz

TZ=pytz.timezone("Asia/Taipei")


class VisitcountSpider(scrapy.Spider):
    name = "visitcount"
	
    allowed_domains = ["http://khvillages.khcc.gov.tw"]
    url_base = "http://khvillages.khcc.gov.tw/"

    def __init__(self):
        self.created_on = datetime.datetime.now(TZ)

	settings = get_project_settings()
        self.is_chromespider = settings.get("CHROME_SPIDER",False)
        self.url_pat1 = 'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4001&IDK=2&AP=$4001_SK--1^$4001_SK2--1^$4001_PN-%d^$4001_HISTORY-0'
        self.url_pat2 = 'http://khvillages.khcc.gov.tw/home02.aspx?ID=$4011&IDK=2&AP=$4011_SK-^$4011_SK2--1^$4011_PN-%d^$4011_HISTORY-0'
        self.url_pat1_index = 1
        self.url_pat2_index = 1
        self.url_pats = [self.url_pat1, self.url_pat2]

        self.data_least = 2066

        if self.is_chromespider:
            from selenium import webdriver
            chrome_bin_path = os.environ.get('CHROME_BIN', "")
            webdriver.ChromeOptions.binary_location = chrome_bin_path
            self.driver = webdriver.Chrome()
            entry_url = ["http://khvillages.khcc.gov.tw/home02.aspx?ID=$4002&IDK=2&EXEC=L&AP=$4002_SK3-115", "http://khvillages.khcc.gov.tw/home02.aspx?ID=$4012&IDK=2&EXEC=L"]
            for url in entry_url:
                self.driver.get(url)


    def start_requests(self):
        for p in self.url_pats:
            url = p % 1
            yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)


    def parse_url(self, response):

        if self.is_chromespider:
            self.driver.get(response.url)
            ax = self.driver.find_elements_by_xpath("//a")
        else:
            ax = response.xpath("//a")

        hrefs = []
        for a in ax:
            if self.is_chromespider:
                href = a.get_attribute("href")
            else:
                try:
                    href = a.xpath("./@href")[0].extract()
                except:
                    pass

            if href:
                hrefs.append(href)


        hrefs = [url for url in hrefs if(("DATA=" in url) and ("_HISTORY-" in url))]

        comp = re.compile("^.*DATA=(\d+)&AP.*$")

        urls = []
        for href in hrefs:
            m = comp.match(href)
            if m:
                if int(m.group(1)) >= self.data_least:
                    urls.append(href)


        if len(urls) > 0:
            if not self.is_chromespider:
                urls = [urlparse.urljoin(self.allowed_domains[0],x) for x in urls]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            
            if "4011_HISTORY" in response.url:
                self.url_pat1_index += 1
                next_url = self.url_pat1 % self.url_pat1_index
            else:
                self.url_pat2_index += 1
                next_url = self.url_pat2 % self.url_pat2_index

            yield scrapy.Request(url=next_url, callback=self.parse_url, dont_filter=True)


    def parse(self, response):
        location_1 = response.xpath("//meta[@name='DC.Title']/@content")[0].extract()

        if u"左營" in location_1:
            location = u"左營"
        else:
            location = u"鳳山"

        self.logger.debug('location: %s' % location)

        address_1 = response.xpath("//meta[@name='DC.Subject']/@content")[0].extract() 
        address = re.match(ur".*村(.*)$",address_1).group(1)
        self.logger.debug('address: %s' % address)

        count_1 = response.xpath("//span[@style='color:#a4a4a4']/text()")[0].extract()
        count = re.match(ur".*已有(.*)人瀏覽.*$",count_1).group(1)
        self.logger.debug('count: %s' % count)

        yield {'location':location,
                'address':address,
                'count':count,
                'created_on':self.created_on
                }
